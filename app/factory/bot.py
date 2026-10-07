"""Telegram bot (shop 3, funnel) — currently a stub.

Checks that it has everything needed to work: the token is accepted by Telegram,
access to the pd schema exists. Then it waits while maintaining a heartbeat.
The real bot will replace run(); it will also process the mini_audit_store buffer.
"""

from __future__ import annotations

import json
import logging
import os
import signal
import time
import urllib.error
import urllib.request

import psycopg

from . import health
from .db import connect

log = logging.getLogger("factory.bot")
running = True


def stop(*_):
    global running
    running = False


def telegram_me(token: str) -> str:
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/getMe", timeout=15) as r:
        data = json.load(r)
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram refused"))
    return data["result"]["username"]


def self_check(token: str) -> None:
    with connect() as conn:
        n = conn.execute("SELECT count(*) FROM pd.telegram_links").fetchone()[0]
    log.info("access to pd confirmed, consents: %d", n)
    try:
        log.info("Telegram accepted the token: @%s", telegram_me(token))
    except urllib.error.HTTPError as e:
        log.error("Telegram rejected the token: HTTP %s", e.code)  # we do not log the token itself
    except (urllib.error.URLError, TimeoutError, RuntimeError) as e:
        log.error("Telegram is unavailable: %s", e)


def run() -> None:
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")
    checked = False
    while running:
        if not checked:
            try:
                self_check(token)
                checked = True
                log.info("bot stub: funnel logic is not implemented yet")
            except psycopg.OperationalError as e:
                log.error("no connection to the database: %s", e)  # no heartbeats — bot is unhealthy
        if checked:
            health.beat()
        time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run()