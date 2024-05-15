import argparse

from update_toml.models.user_input import UserInput


class CLIInputHandler:
    def parse(self) -> UserInput:
        parser = argparse.ArgumentParser(
            prog="UpdateTOML",
            description="Update the value in a TOML file from a CLI",
        )

        parser.add_argument(
            "-f",
            "--file",
            help="The path to the .toml file to update",
            default="pyproject.toml",
        )
        parser.add_argument(
            "-p",
            "--path",
            help="Path in the attribute in the TOML file to update (ex. project.version or tool.poetry.version)",
            required=True,
            type=str,
        )
        parser.add_argument(
            "-v",
            "--value",
            help="The value to set the path to in the TOML file",
            required=True,
            type=str,
        )

        args: argparse.Namespace = parser.parse_args()

        return UserInput(args.file, args.path, args.value)
