#!/usr/bin/env

import logging
import os

from update_toml.cli_input_handler import CLIInputHandler
from update_toml.interfaces.input_handler import InputHandler
from update_toml.models.user_input import UserInput
from update_toml.toml_file import TOMLFile

logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=os.environ.get("LOGLEVEL", "INFO"),
)


def main() -> None:
    input_handler: InputHandler = CLIInputHandler()
    args: UserInput = input_handler.parse()

    toml_file = TOMLFile(args.toml_path)

    toml_file.load()
    logging.info(f"Loaded {args.toml_path}.")

    toml_file.update(args.path, args.value)
    logging.info(f"Updated {args.path} to '{args.value}'.")

    toml_file.save()
    logging.info(f"Saved update values to {args.toml_path}.")


if __name__ == "__main__":
    main()
