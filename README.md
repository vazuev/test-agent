# test-agent

![Tests](https://github.com/vazuev/test-agent/actions/workflows/tests.yml/badge.svg)

This repository is maintained autonomously by dev-agent: a Claude Code worker that picks up Linear tickets labeled `agent` and implements them.

## Design docs

- [MYW-13: Calendar agent with a Telegram interface](docs/design/MYW-13-calendar-telegram-agent.md) —
  architecture proposal for an agent that manages a calendar and talks to the
  user interactively over Telegram.

## hello.py

A smoke-test CLI. Run it with:

```
python3 hello.py
```

It prints `Hello, dev-agent!`.

## Tasks with Telegram status notifications

`task.py` defines a minimal in-memory `Task` model (`id`, `title`, `status`)
with a `status` of `todo` / `in_progress` / `done`. Calling
`task.update_status(new_status)` changes the status and sends a best-effort
Telegram notification (`Задача "<title>": <old> → <new>`) via
`telegram_notifier.send_message`, which talks to the Telegram Bot API
(`https://api.telegram.org/bot<TOKEN>/sendMessage`) using only the standard
library.

Configure the bot via environment variables (never hardcoded):

```
export TELEGRAM_BOT_TOKEN=your-bot-token
export TELEGRAM_CHAT_ID=your-chat-id
```

If either variable is unset, or the Telegram API call fails, the
notification is skipped/logged and the status change still succeeds — it
never raises. Tests mock the HTTP call, so no real token is required to run
the test suite.

### Tests

```
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

## Docker

The agent runs in a Docker container. The same image is used to run the
test suite, so CI exercises the exact environment the agent runs in.

Build the image:

```
docker build -t test-agent .
```

Run the agent:

```
docker run --rm test-agent
```

Run the test suite inside the container:

```
docker run --rm test-agent python -m pytest
```

## CI

GitHub Actions (`.github/workflows/tests.yml`) builds the Docker image and
runs the test suite inside it on every push to `main` and on every pull
request.
