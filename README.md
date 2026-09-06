# test-agent

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

### Tests

```
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```
