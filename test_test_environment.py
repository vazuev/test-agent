from pathlib import Path

ROOT = Path(__file__).parent
DOCKERFILE = ROOT / "Dockerfile"
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"


def test_dockerfile_exists():
    assert DOCKERFILE.is_file(), "missing Dockerfile: agent must run in Docker"


def test_dockerfile_defines_runnable_image():
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "FROM python" in text
    assert "CMD" in text


def test_github_actions_workflow_exists():
    assert WORKFLOW.is_file(), f"missing GitHub Actions workflow: {WORKFLOW}"


def test_github_actions_workflow_runs_tests():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pytest" in text
    assert "on:" in text
    assert "pull_request" in text
