from dataclasses import dataclass


@dataclass(frozen=True)
class UserInput:
    command: str
    toml_path: str
    path: str
    value: str | None = None
