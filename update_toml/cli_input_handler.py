import argparse
from update_toml.models.user_input import UserInput


class CLIInputHandler:
    def parse(self) -> UserInput:
        parser = argparse.ArgumentParser(
            prog="UpdateTOML",
            description="Update or check the existence of a value in a TOML file from a CLI",
        )

        subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

        # Subparser for the update command
        update_parser = subparsers.add_parser(
            "update", help="Update a value in the TOML file"
        )
        update_parser.add_argument(
            "-f",
            "--file",
            help="The path to the .toml file to update",
            default="pyproject.toml",
        )
        update_parser.add_argument(
            "-p",
            "--path",
            help="Path in the attribute in the TOML file to update (ex. project.version or tool.poetry.version)",
            required=True,
            type=str,
        )
        update_parser.add_argument(
            "-v",
            "--value",
            help="The value to set the path to in the TOML file",
            required=True,
            type=str,
        )

        # Subparser for the exists command
        exists_parser: argparse.ArgumentParser = subparsers.add_parser(
            "exists", help="Check if a path exists in the TOML file"
        )
        exists_parser.add_argument(
            "-f",
            "--file",
            help="The path to the .toml file to check",
            default="pyproject.toml",
        )
        exists_parser.add_argument(
            "-p",
            "--path",
            help="Path in the attribute in the TOML file to check (ex. project.version or tool.poetry.version)",
            required=True,
            type=str,
        )

        # Subparser for the exists command
        get_value_parser: argparse.ArgumentParser = subparsers.add_parser(
            "get", help="Get a value from a TOML file."
        )
        get_value_parser.add_argument(
            "-f",
            "--file",
            help="The path to the .toml file",
            default="pyproject.toml",
        )
        get_value_parser.add_argument(
            "-p",
            "--path",
            help="Path of the attribute in the TOML file to get (ex. project.version or tool.poetry.version)",
            required=True,
            type=str,
        )

        args: argparse.Namespace = parser.parse_args()

        return UserInput(
            command=args.command,
            toml_path=args.file,
            path=args.path,
            value=args.value if args.command == "update" else None,
        )
