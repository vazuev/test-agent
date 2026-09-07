"""Minimal in-memory Task model with Telegram status-change notifications."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from itertools import count

import telegram_notifier

logger = logging.getLogger(__name__)

VALID_STATUSES = ("todo", "in_progress", "done")

_id_counter = count(1)


@dataclass
class Task:
    """A task with an identifier, a title and a status.

    Status changes are made through :meth:`update_status`, which also sends
    a best-effort Telegram notification about the transition.
    """

    title: str
    status: str = "todo"
    id: int = field(default_factory=lambda: next(_id_counter))

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status {self.status!r}; must be one of {VALID_STATUSES}"
            )

    def update_status(self, new_status: str) -> None:
        """Change the task's status and notify Telegram about the change.

        Raises ValueError for an unknown status. The Telegram notification
        is best-effort: failures are logged but never raised, so a status
        change always succeeds once validated.
        """
        if new_status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status {new_status!r}; must be one of {VALID_STATUSES}"
            )

        old_status = self.status
        self.status = new_status

        if old_status == new_status:
            return

        text = f'Задача "{self.title}": {old_status} → {new_status}'
        try:
            telegram_notifier.send_message(
                text,
                token=os.environ.get("TELEGRAM_BOT_TOKEN"),
                chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
            )
        except Exception:  # pragma: no cover - defense in depth
            logger.exception("Unexpected error while sending Telegram notification")
