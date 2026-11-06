import sys

from tomlkit.exceptions import TOMLKitError

from update_toml.cli_input_handler import CLIInputHandler
from update_toml.toml_file import TOMLFile


def main() -> None:
    args = CLIInputHandler().parse()
    try:
        toml_file = TOMLFile(args.toml_path)
        toml_file.load()
        if args.command == "update":
            assert args.value is not None  # argparse requires --value
            toml_file.update(args.path, args.value)
            toml_file.save()
        elif args.command == "exists":
            print(toml_file.path_exists(args.path))
        else:
            print(toml_file.get_value_safe(args.path))
    except (OSError, TOMLKitError, KeyError, ValueError, TypeError) as error:
        print(f"update-toml: error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
