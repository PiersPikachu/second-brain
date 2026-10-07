"""Kanban in PostgreSQL: claim a card, complete it, return it to the queue, send it to the isolator.

Worker's order of operations with a card:
  1. claim()   — short transaction: the card becomes in_progress (FOR UPDATE SKIP LOCKED);
  2. processing — outside the transaction (long API calls do not hold locks);
  3. complete() — one transaction: new cards into the next buffers + done.
     If the next buffer is full, the card is returned to the queue (pull system:
     a shop does not produce more than the consumer can accept).
The part stops, not the line: a failure of one card does not stop the worker.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Any

from psycopg import Connection, errors
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

MAX_ATTEMPTS = 3
RETRY_BACKOFF = dt.timedelta(minutes=5)      # multiplied by the attempt number
FULL_BUFFER_DELAY = dt.timedelta(minutes=1)  # wait while the consumer drains the buffer
STALE_AFTER = dt.timedelta(minutes=30)       # in_progress longer — the worker died


@dataclass
class WorkItem:
    id: int
    buffer_code: str
    payload: dict
    attempts: int
    priority: int


@dataclass
class Card:
    """A new card into the next buffer."""
    buffer_code: str
    payload: dict
    priority: int = 0
    scheduled_for: dt.datetime | None = None


@dataclass
class Result:
    children: list[Card] = field(default_factory=list)


class Defect(Exception):
    """A defect found by the check (QC): the card immediately goes to the isolator."""

    def __init__(self, check_code: str, details: dict | None = None):
        super().__init__(check_code)
        self.check_code = check_code
        self.details = details or {}


class BufferFull(Exception):
    pass


def buffers_of(conn: Connection, workshop: str) -> list[str]:
    rows = conn.execute(
        """SELECT b.code FROM line.buffers b
           JOIN line.workshops w ON w.id = b.workshop_id
           WHERE w.code = %s ORDER BY b.code""", (workshop,)).fetchall()
    return [r[0] for r in rows]


def claim(conn: Connection, buffers: list[str], worker_id: str) -> WorkItem | None:
    with conn.transaction():
        row = conn.execute(
            """UPDATE line.work_items
               SET status = 'in_progress', started_at = now(),
                   attempts = attempts + 1, locked_by = %s
               WHERE id = (SELECT id FROM line.work_items
                           WHERE buffer_code = ANY(%s) AND status = 'queued'
                             AND scheduled_for <= now()
                           ORDER BY priority DESC, scheduled_for
                           FOR UPDATE SKIP LOCKED LIMIT 1)
               RETURNING id, buffer_code, payload, attempts, priority""",
            (worker_id, buffers)).fetchone()
    if row is None:
        return None
    return WorkItem(*row)


def enqueue(conn: Connection, card: Card, parent_id: int | None = None) -> int:
    try:
        with conn.transaction():
            return conn.execute(
                """INSERT INTO line.work_items (buffer_code, payload, priority, scheduled_for, parent_id)
                   VALUES (%s, %s, %s, coalesce(%s, now()), %s) RETURNING id""",
                (card.buffer_code, Jsonb(card.payload), card.priority, card.scheduled_for,
                 parent_id)).fetchone()[0]
    except errors.RaiseException as e:
        if "kanban limit reached" in str(e):
            raise BufferFull(card.buffer_code) from e
        raise


def complete(conn: Connection, item: WorkItem, result: Result) -> None:
    """Child cards and done — atomically. Full buffer — the card waits in the queue."""
    try:
        with conn.transaction():
            for card in result.children:
                enqueue(conn, card, parent_id=item.id)
            conn.execute(
                """UPDATE line.work_items SET status = 'done', finished_at = now(), locked_by = NULL
                   WHERE id = %s AND status = 'in_progress'""", (item.id,))
    except BufferFull:
        with conn.transaction():
            conn.execute(
                """UPDATE line.work_items
                   SET status = 'queued', locked_by = NULL, started_at = NULL,
                       attempts = attempts - 1, scheduled_for = now() + %s
                   WHERE id = %s""", (FULL_BUFFER_DELAY, item.id))
        raise


def quarantine(conn: Connection, item_id: int, check_code: str, details: dict,
               decision: str = "escalate") -> None:
    with conn.transaction():
        conn.execute(
            """UPDATE line.work_items SET status = 'quarantined', finished_at = now(), locked_by = NULL
               WHERE id = %s""", (item_id,))
        conn.execute(
            """INSERT INTO line.defects (work_item_id, check_code, details, decided_by, decision)
               VALUES (%s, %s, %s, 'auto', %s)""", (item_id, check_code, Jsonb(details), decision))


def fail(conn: Connection, item: WorkItem, error: BaseException) -> str:
    """Processing failure: retry with a delay, after MAX_ATTEMPTS — isolator. Returns the outcome."""
    details = {"error": type(error).__name__, "message": str(error)[:500], "attempts": item.attempts}
    if isinstance(error, Defect):
        quarantine(conn, item.id, error.check_code, {**details, **error.details})
        return "quarantined"
    if item.attempts >= MAX_ATTEMPTS:
        quarantine(conn, item.id, "handler_failed", details)
        return "quarantined"
    with conn.transaction():
        conn.execute(
            """UPDATE line.work_items
               SET status = 'queued', locked_by = NULL, started_at = NULL,
                   scheduled_for = now() + %s
               WHERE id = %s""", (RETRY_BACKOFF * item.attempts, item.id))
    return "retry"


def expire(conn: Connection, buffers: list[str]) -> int:
    """Cards older than the buffer's max_age — defect (stale lead, outdated mini-audit)."""
    with conn.transaction():
        rows = conn.execute(
            """WITH old AS (
                 UPDATE line.work_items w SET status = 'expired', finished_at = now()
                 FROM line.buffers b
                 WHERE w.buffer_code = b.code AND b.code = ANY(%s) AND b.max_age IS NOT NULL
                   AND w.status = 'queued' AND w.enqueued_at < now() - b.max_age
                 RETURNING w.id, b.max_age)
               INSERT INTO line.defects (work_item_id, check_code, details, decided_by, decision, resolved_at)
               SELECT id, 'expired', jsonb_build_object('max_age', max_age::text), 'auto', 'discard', now()
               FROM old RETURNING work_item_id""", (buffers,)).fetchall()
    return len(rows)


def recover_stale(conn: Connection, buffers: list[str]) -> int:
    """Cards abandoned by a crashed worker: back to the queue or to the isolator."""
    with conn.transaction():
        stale = conn.execute(
            """SELECT id, attempts FROM line.work_items
               WHERE buffer_code = ANY(%s) AND status = 'in_progress' AND started_at < now() - %s
               FOR UPDATE SKIP LOCKED""", (buffers, STALE_AFTER)).fetchall()
    for item_id, attempts in stale:
        if attempts >= MAX_ATTEMPTS:
            quarantine(conn, item_id, "stale", {"attempts": attempts})
        else:
            with conn.transaction():
                conn.execute(
                    """UPDATE line.work_items SET status = 'queued', locked_by = NULL, started_at = NULL
                       WHERE id = %s AND status = 'in_progress'""", (item_id,))
    return len(stale)


def buffer_stats(conn: Connection) -> list[dict[str, Any]]:
    with conn.cursor(row_factory=dict_row) as cur:
        return cur.execute("SELECT * FROM line.buffer_stats ORDER BY code").fetchall()