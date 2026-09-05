# test-agent

This repository is maintained autonomously by dev-agent: a Claude Code worker that picks up Linear tickets labeled `agent` and implements them.

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
