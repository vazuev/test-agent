import pytest

import task as task_module
from task import Task


@pytest.fixture
def fake_send(monkeypatch):
    calls = []

    def fake(text, *, token, chat_id):
        calls.append({"text": text, "token": token, "chat_id": chat_id})
        return True

    monkeypatch.setattr(task_module.telegram_notifier, "send_message", fake)
    return calls


def test_task_created_with_default_status():
    t = Task(title="Write tests")
    assert t.status == "todo"


def test_task_rejects_invalid_initial_status():
    with pytest.raises(ValueError):
        Task(title="Bad", status="bogus")


def test_update_status_changes_status(fake_send):
    t = Task(title="Ship feature")
    t.update_status("in_progress")
    assert t.status == "in_progress"


def test_update_status_rejects_invalid_status(fake_send):
    t = Task(title="Ship feature")
    with pytest.raises(ValueError):
        t.update_status("not_a_status")
    assert t.status == "todo"
    assert fake_send == []


def test_update_status_sends_telegram_notification(fake_send, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    t = Task(title="Deploy app")
    t.update_status("done")

    assert len(fake_send) == 1
    call = fake_send[0]
    assert call["text"] == 'Задача "Deploy app": todo → done'
    assert call["token"] == "test-token"
    assert call["chat_id"] == "test-chat"


def test_update_status_to_same_status_does_not_notify(fake_send):
    t = Task(title="No-op")
    t.update_status("todo")
    assert fake_send == []


def test_update_status_survives_notifier_failure(monkeypatch):
    def failing_send(text, *, token, chat_id):
        raise RuntimeError("boom")

    monkeypatch.setattr(task_module.telegram_notifier, "send_message", failing_send)

    t = Task(title="Resilient task")
    t.update_status("in_progress")

    assert t.status == "in_progress"


def test_update_status_works_without_env_vars(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    t = Task(title="No config")
    t.update_status("in_progress")

    assert t.status == "in_progress"
