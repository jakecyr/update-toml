from __future__ import annotations

import json
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

import tomlkit as toml
from tomlkit.toml_document import TOMLDocument

from update_toml.exceptions.file_not_loaded_exception import FileNotLoadedException


class TOMLFile:
    def __init__(self, file_path: str | Path = "pyproject.toml") -> None:
        self._file_path = file_path
        self._contents: TOMLDocument | None = None

    def load(self) -> None:
        with open(self._file_path, encoding="utf-8", newline="") as f:
            self._contents = toml.load(f)

    def _document(self) -> TOMLDocument:
        if self._contents is None:
            raise FileNotLoadedException("load has not yet been called")
        return self._contents

    @staticmethod
    def _parts(path: str) -> list[str]:
        parts = path.split(".")
        if not path or any(not part for part in parts):
            raise ValueError("Path must contain non-empty dot-separated keys")
        return parts

    def to_json(self) -> str:
        return json.dumps(self._document())

    def update(self, path: str, new_value: Any) -> None:
        current: Any = self._document()
        parts = self._parts(path)
        for part in parts[:-1]:
            if not isinstance(current, MutableMapping) or part not in current:
                raise KeyError(f"Parent table for '{path}' does not exist")
            current = current[part]
        if not isinstance(current, MutableMapping):
            raise TypeError(f"Parent of '{path}' is not a table")
        current[parts[-1]] = new_value

    def path_exists(self, path: str) -> bool:
        try:
            self.get_value(path)
            return True
        except KeyError:
            return False

    def get_value_safe(self, path: str) -> Any:
        try:
            return self.get_value(path)
        except KeyError:
            return ""

    def get_value(self, path: str) -> Any:
        current: Any = self._document()
        for part in self._parts(path):
            if not isinstance(current, MutableMapping) or part not in current:
                raise KeyError(path)
            current = current[part]
        return current

    def save(self) -> None:
        # Serialize before opening the file so serialization errors cannot truncate it.
        contents = toml.dumps(self._document())
        with open(self._file_path, "w", encoding="utf-8", newline="") as f:
            f.write(contents)
