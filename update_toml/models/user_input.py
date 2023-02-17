from dataclasses import dataclass


@dataclass
class UserInput:
    toml_path: str
    path: str
    value: str
