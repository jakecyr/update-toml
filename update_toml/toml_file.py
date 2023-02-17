from typing import Any, Dict, List, Optional
import toml
from update_toml.exceptions.file_not_loaded_exception import (
    FileNotLoadedException,
)
import json
from update_toml.utils.get_parent_object import find_parent_path


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

        parent_object = find_parent_path(path_parts, self._contents)
        property_to_update = path_parts[0]
        parent_object[property_to_update] = new_value

    def save(self) -> None:
        with open(self._file_path, "w") as f:
            toml.dump(self._contents, f)
