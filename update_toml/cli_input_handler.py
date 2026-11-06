import argparse

from update_toml.models.user_input import UserInput


class CLIInputHandler:
    def parse(self) -> UserInput:
        parser = argparse.ArgumentParser(
            prog="update-toml",
            description="Update or inspect a value in a TOML file.",
        )
        subparsers = parser.add_subparsers(dest="command", required=True)
        for command in ("update", "get", "exists"):
            subparser = subparsers.add_parser(
                command, help=f"{command.capitalize()} a value"
            )
            subparser.add_argument(
                "-f",
                "--file",
                default="pyproject.toml",
                help="TOML file (default: pyproject.toml)",
            )
            subparser.add_argument(
                "-p",
                "--path",
                required=True,
                help="Dot-separated keys, e.g. project.version",
            )
            if command == "update":
                subparser.add_argument(
                    "-v", "--value", required=True, help="String value to write"
                )
        args = parser.parse_args()
        return UserInput(
            args.command, args.file, args.path, getattr(args, "value", None)
        )
