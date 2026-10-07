"""Buffer handlers: buffer code -> function(WorkItem) -> Result.

While the shops are not implemented, stubs live here. A stub does not discard cards:
it sends them to the isolator with check_code='not_implemented', from where they can be
returned to the queue when a real handler appears.
A handler does not write to the database itself — it returns a Result with new cards,
and kanban.complete() saves them together with the done mark in a single transaction.
Result checking (QC) — via the kanban.Defect exception.
"""

from __future__ import annotations

from typing import Callable

from .kanban import Defect, Result, WorkItem

Handler = Callable[[WorkItem], Result]


def not_implemented(item: WorkItem) -> Result:
    raise Defect("not_implemented", {"buffer": item.buffer_code})


HANDLERS: dict[str, Handler] = {
    # lead warehouse -> shop 2: mini-audit from a category measurement slice -> mini_audit_store
    "leads_store": not_implemented,
    # mini-audit warehouse -> shop 3 (bot): sending the mini-audit to Telegram
    "mini_audit_store": not_implemented,
    # onboarding queue -> shop 5: first subscriber measurement within 24 hours
    "onboarding": not_implemented,
}


def handler_for(buffer_code: str) -> Handler:
    return HANDLERS.get(buffer_code, not_implemented)