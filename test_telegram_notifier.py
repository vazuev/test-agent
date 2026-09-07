import urllib.error

import pytest

import telegram_notifier


def test_send_message_skips_without_token(monkeypatch, caplog):
    with caplog.at_level("WARNING"):
        result = telegram_notifier.send_message("hi", token=None, chat_id="123")
    assert result is False
    assert "skipped" in caplog.text


def test_send_message_skips_without_chat_id(caplog):
    with caplog.at_level("WARNING"):
        result = telegram_notifier.send_message("hi", token="tok", chat_id=None)
    assert result is False
    assert "skipped" in caplog.text


def test_send_message_success(monkeypatch):
    calls = {}

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

    def fake_urlopen(request, timeout=None):
        calls["url"] = request.full_url
        calls["data"] = request.data
        return FakeResponse()

    monkeypatch.setattr(telegram_notifier.urllib.request, "urlopen", fake_urlopen)

    result = telegram_notifier.send_message("hello", token="tok", chat_id="42")

    assert result is True
    assert calls["url"] == "https://api.telegram.org/bottok/sendMessage"
    assert b"chat_id=42" in calls["data"]


def test_send_message_handles_http_error(monkeypatch, caplog):
    def fake_urlopen(request, timeout=None):
        raise urllib.error.HTTPError(request.full_url, 500, "Internal Error", {}, None)

    monkeypatch.setattr(telegram_notifier.urllib.request, "urlopen", fake_urlopen)

    with caplog.at_level("WARNING"):
        result = telegram_notifier.send_message("hello", token="tok", chat_id="42")

    assert result is False
    assert "failed" in caplog.text


def test_send_message_handles_network_error(monkeypatch, caplog):
    def fake_urlopen(request, timeout=None):
        raise urllib.error.URLError("network unreachable")

    monkeypatch.setattr(telegram_notifier.urllib.request, "urlopen", fake_urlopen)

    with caplog.at_level("WARNING"):
        result = telegram_notifier.send_message("hello", token="tok", chat_id="42")

    assert result is False
    assert "failed" in caplog.text


def test_send_message_handles_non_2xx_status(monkeypatch, caplog):
    class FakeResponse:
        status = 403

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            return False

    def fake_urlopen(request, timeout=None):
        return FakeResponse()

    monkeypatch.setattr(telegram_notifier.urllib.request, "urlopen", fake_urlopen)

    with caplog.at_level("WARNING"):
        result = telegram_notifier.send_message("hello", token="tok", chat_id="42")

    assert result is False
    assert "status" in caplog.text
