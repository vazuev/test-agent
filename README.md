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
