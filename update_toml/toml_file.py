import json
from typing import Any, Dict, List, Optional

import toml

from update_toml.exceptions.file_not_loaded_exception import \
    FileNotLoadedException


class TOMLFile:
    def __init__(self, file_path: str) -> None:
        self._file_path: str = file_path
        self._contents: Optional[Dict[str, Any]] = None

    def load(self) -> None:
        with open(self._file_path) as f:
            self._contents = toml.load(f)

    def to_json(self) -> str:
        if self._contents is None:
            raise FileNotLoadedException("load has not yet been called")

        return json.dumps(self._contents)

    def update(self, path: str, new_value: str) -> None:
        if self._contents is None:
            raise FileNotLoadedException("load has not yet been called")

        path_parts: List[str] = path.split(".")

        if len(path_parts) < 2:
            raise ValueError(
                "Path should have at least two parts (ex. project.version)"
            )

        parent_object = self._get_parent_object(path_parts, self._contents)
        property_to_update = path_parts[0]
        parent_object[property_to_update] = new_value

    def get_value(self, path: str) -> str:
        path_parts: List[str] = path.split(".")
        return self._get_value(path_parts, self._contents)

    def save(self) -> None:
        with open(self._file_path, "w") as f:
            toml.dump(self._contents, f)

    def _get_parent_object(self, path_parts: List[str], object: Any):
        if len(path_parts) > 1:
            current_path = path_parts.pop(0)
            return self._get_parent_object(path_parts, object[current_path])
        else:
            return object

    def _get_value(self, path_parts: List[str], object: Any):
        if len(path_parts) > 1:
            current_path = path_parts.pop(0)
            return self._get_value(path_parts, object[current_path])
        else:
            return object[path_parts[0]]
