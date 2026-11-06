import subprocess
import sys
from pathlib import Path

import pytest


def cli(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "update_toml.main", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture
def project(tmp_path: Path) -> Path:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nversion = "1"\n', encoding="utf-8"
    )
    return tmp_path


def test_commands_and_empty_value(project: Path) -> None:
    assert cli("update", "-p", "project.version", "-v", "", cwd=project).returncode == 0
    result = cli("get", "-p", "project.version", cwd=project)
    assert (result.returncode, result.stdout) == (0, "\n")
    assert cli("exists", "-p", "project.version", cwd=project).stdout == "True\n"
    assert cli("exists", "-p", "project.missing", cwd=project).stdout == "False\n"
    assert cli("get", "-p", "project.missing", cwd=project).stdout == "\n"


def test_file_argument(project: Path) -> None:
    other = project / "other.toml"
    other.write_text('value = "hello"\n', encoding="utf-8")
    assert cli("get", "-f", str(other), "-p", "value", cwd=project).stdout == "hello\n"


@pytest.mark.parametrize("args", [(), ("update",), ("unknown",)])
def test_usage_errors(project: Path, args: tuple[str, ...]) -> None:
    result = cli(*args, cwd=project)
    assert result.returncode == 2
    assert "usage:" in result.stderr and "Traceback" not in result.stderr


def test_runtime_errors(project: Path) -> None:
    for args in [
        ("get", "-p", "x", "-f", "missing"),
        ("get", "-p", "a..b"),
        ("update", "-p", "missing.x", "-v", "1"),
    ]:
        result = cli(*args, cwd=project)
        assert result.returncode == 1
        assert (
            "update-toml: error:" in result.stderr and "Traceback" not in result.stderr
        )
    (project / "pyproject.toml").write_text("invalid = [", encoding="utf-8")
    result = cli("get", "-p", "invalid", cwd=project)
    assert result.returncode == 1 and "Traceback" not in result.stderr
