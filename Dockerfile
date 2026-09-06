# Runtime/test image for the dev-agent.
#
# Includes dev dependencies (currently just pytest) so the same image can be
# used both to run the agent and to run the test suite in CI:
#   docker build -t test-agent .
#   docker run --rm test-agent               # runs the agent (hello.py)
#   docker run --rm test-agent python -m pytest   # runs the test suite
FROM python:3.12-slim

WORKDIR /app

COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

CMD ["python", "hello.py"]
