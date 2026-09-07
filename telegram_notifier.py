"""Minimal Telegram Bot API client for sending notification messages.

Configuration (bot token, chat id) comes from environment variables so that
no secrets are hardcoded or committed:

    TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID

If either variable is missing, ``send_message`` skips the network call and
returns ``False`` instead of raising, so the module stays importable and
testable without a real bot. Network/API errors are caught and logged, never
propagated, so callers can treat notifications as best-effort.
"""

from __future__ import annotations

import logging
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

API_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"


def send_message(text: str, *, token: str | None, chat_id: str | None) -> bool:
    """Send ``text`` to ``chat_id`` via the Telegram Bot API.

    Returns True on success, False if the message was skipped or failed.
    Never raises: this is a best-effort notification, not a critical path.
    """
    if not token or not chat_id:
        logger.warning(
            "Telegram notification skipped: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID not set"
        )
        return False

    url = API_URL_TEMPLATE.format(token=token)
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status = getattr(response, "status", 200)
            if status >= 400:
                logger.warning("Telegram API returned status %s", status)
                return False
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        logger.warning("Telegram notification failed: %s", exc)
        return False
