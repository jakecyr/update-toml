from typing import Any, List


def find_parent_path(path_parts: List[str], object: Any):
    if len(path_parts) > 1:
        current_path = path_parts.pop(0)
        return find_parent_path(path_parts, object[current_path])
    else:
        return object
