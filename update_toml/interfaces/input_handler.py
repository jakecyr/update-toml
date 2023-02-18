from typing import Protocol

from update_toml.models.user_input import UserInput


class InputHandler(Protocol):
    def parse(self) -> UserInput:
        pass
