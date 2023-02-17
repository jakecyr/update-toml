#!/usr/bin/env

from update_toml.cli_input_handler import CLIInputHandler
from update_toml.interfaces.input_handler import InputHandler

from update_toml.models.user_input import UserInput
from update_toml.toml_file import TOMLFile


def main() -> None:
    input_handler: InputHandler = CLIInputHandler()
    args: UserInput = input_handler.parse()

    toml_file = TOMLFile(args.toml_path)

    toml_file.load()
    toml_file.update(args.path, args.value)
    toml_file.save()


if __name__ == "__main__":
    main()
