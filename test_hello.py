import subprocess
import sys


def test_hello_prints_greeting():
    result = subprocess.run(
        [sys.executable, "hello.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "Hello, dev-agent!"
