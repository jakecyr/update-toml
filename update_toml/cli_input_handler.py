import argparse

from update_toml.models.user_input import UserInput


class CLIInputHandler:
    def parse(self) -> UserInput:
        parser = argparse.ArgumentParser(
            prog="UpdateTOML",
            description="Update the value in a TOML file from a CLI",
        )

        parser.add_argument(
            "toml_path", help="The path to the .toml file to update"
        )
        parser.add_argument(
            "-p",
            "--path",
            help="Path in the TOML to update (ex. project.version)",
        )
        parser.add_argument(
            "-v", "--value", help="The value to set the path to"
        )

        args: argparse.Namespace = parser.parse_args()

        return UserInput(args.toml_path, args.path, args.value)
