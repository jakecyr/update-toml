import json
from unittest.mock import MagicMock, mock_open, patch

import pytest
from pytest import fixture

from update_toml.exceptions.file_not_loaded_exception import FileNotLoadedException
from update_toml.toml_file import TOMLFile

TEST_FILE_PATH = "pyproject-test.toml"

TEST_TOML_CONTENTS = """
[project]
name = "update_toml"
authors = [
    {name = "Jake Cyr", email = "cyrjake@gmail.com"},
]
version = "0.0.1"
description = "Update a toml value from a CLI"
readme = "README.md"
requires-python = ">=3.7"
keywords = ["toml", "requirements", "update"]
license = {text = "MIT"}
classifiers = [
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
]
dependencies = [
  "toml"
]
"""


file_mock = MagicMock()
file_mock.read.return_value = "test"


@fixture
def toml_file() -> TOMLFile:
    return TOMLFile(TEST_FILE_PATH)


def test_toml_file_load_loads_contents(toml_file: TOMLFile) -> None:
    with patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS)) as mock:
        toml_file.load()

    assert mock.call_args_list[0].args[0] == TEST_FILE_PATH
    assert toml_file._contents is not None


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_to_json_works(toml_file: TOMLFile) -> None:
    toml_file.load()

    try:
        json.loads(toml_file.to_json())
    except:
        pytest.fail("Invalid JSON received from to_json method")


def test_to_json_raises_error_if_not_loaded(toml_file: TOMLFile) -> None:
    with pytest.raises(FileNotLoadedException):
        toml_file.to_json()


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_update_updates_the_toml_value(toml_file: TOMLFile) -> None:
    toml_file.load()
    path = "project.version"
    new_value = "10.0.0"

    toml_file.update(path, new_value)
    assert toml_file._contents is not None
    assert toml_file._contents["project"]["version"] == new_value


def test_update_raises_exception_if_not_loaded(toml_file: TOMLFile):
    path = "project.version"
    new_value = "10.0.0"

    with pytest.raises(FileNotLoadedException):
        toml_file.update(path, new_value)


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_update_raises_exception_if_invalid_path(toml_file: TOMLFile) -> None:
    path = "project"
    new_value = "10.0.0"

    toml_file.load()

    with pytest.raises(ValueError):
        toml_file.update(path, new_value)


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_get_value_returns_correct_value(toml_file: TOMLFile) -> None:
    toml_file.load()
    version = toml_file.get_value("project.version")
    assert toml_file._contents is not None
    assert version == toml_file._contents["project"]["version"]


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_get_parent_object(toml_file: TOMLFile) -> None:
    object = toml_file._get_parent_object(
        ["project", "version"], {"project": {"version": "10.0.0"}}
    )

    assert object == {"version": "10.0.0"}


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_save_raises_exception_if_not_loaded(toml_file: TOMLFile) -> None:
    with pytest.raises(ValueError):
        toml_file.save()


@patch("builtins.open")
def test_save_does_not_throw_error(toml_file: TOMLFile) -> None:
    toml_file.load()
    toml_file.save()


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_get_value_safe_does_not_throw_error(toml_file: TOMLFile) -> None:
    toml_file.load()
    path = "test"
    toml_file.get_value_safe(path)


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_path_exists_returns_true_if_exists(toml_file: TOMLFile) -> None:
    toml_file.load()
    path = "project.version"
    assert toml_file.path_exists(path)


@patch("builtins.open", mock_open(read_data=TEST_TOML_CONTENTS))
def test_path_exists_returns_false_if_does_not_exist(toml_file: TOMLFile) -> None:
    toml_file.load()
    assert not toml_file.path_exists("project.versionz")
    assert not toml_file.path_exists("versionz")
    assert not toml_file.path_exists("versionz.version.version")
    assert not toml_file.path_exists("")
