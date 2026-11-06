import json
from pathlib import Path

import pytest

from update_toml.exceptions.file_not_loaded_exception import FileNotLoadedException
from update_toml.toml_file import TOMLFile


@pytest.fixture
def document(tmp_path: Path) -> TOMLFile:
    path = tmp_path / "sample.toml"
    path.write_text(
        '# comment\nroot = "old"\n[project]\nversion = "1" # keep\ncount = 2\n',
        encoding="utf-8",
    )
    result = TOMLFile(path)
    result.load()
    return result


@pytest.mark.parametrize(
    "method,args",
    [
        ("to_json", ()),
        ("update", ("x", "y")),
        ("path_exists", ("x",)),
        ("get_value", ("x",)),
        ("get_value_safe", ("x",)),
        ("save", ()),
    ],
)
def test_requires_load(tmp_path: Path, method: str, args: tuple) -> None:
    with pytest.raises(FileNotLoadedException):
        getattr(TOMLFile(tmp_path / "x"), method)(*args)


def test_read_and_update_preserves_comments(document: TOMLFile, tmp_path: Path) -> None:
    assert document.get_value("project.count") == 2
    assert json.loads(document.to_json())["project"]["version"] == "1"
    document.update("project.version", "")
    document.update("project.new", "value")
    document.update("root", "changed")
    document.save()
    text = (tmp_path / "sample.toml").read_text(encoding="utf-8")
    assert "# comment" in text and "# keep" in text
    document.load()
    assert document.get_value("project.version") == ""
    assert document.get_value("project.new") == "value"
    assert document.get_value("root") == "changed"


@pytest.mark.parametrize(
    "path", ["missing", "project.missing", "root.child", "missing.child"]
)
def test_missing_paths(document: TOMLFile, path: str) -> None:
    assert not document.path_exists(path)
    assert document.get_value_safe(path) == ""
    with pytest.raises(KeyError):
        document.get_value(path)


@pytest.mark.parametrize("path", ["", ".project", "project.", "project..version"])
def test_invalid_paths(document: TOMLFile, path: str) -> None:
    for method in (document.get_value, document.get_value_safe, document.path_exists):
        with pytest.raises(ValueError):
            method(path)
    with pytest.raises(ValueError):
        document.update(path, "x")


def test_missing_or_non_table_parent(document: TOMLFile) -> None:
    with pytest.raises(KeyError):
        document.update("missing.child", "x")
    with pytest.raises(TypeError):
        document.update("root.child", "x")


def test_empty_file_can_be_saved(tmp_path: Path) -> None:
    path = tmp_path / "empty.toml"
    path.write_text("", encoding="utf-8")
    document = TOMLFile(path)
    document.load()
    document.save()
    assert path.read_text(encoding="utf-8") == ""


def test_crlf_preserved(tmp_path: Path) -> None:
    path = tmp_path / "crlf.toml"
    path.write_bytes(b'[project]\r\nversion = "1"\r\n')
    document = TOMLFile(path)
    document.load()
    document.update("project.version", "2")
    document.save()
    assert path.read_bytes() == b'[project]\r\nversion = "2"\r\n'
