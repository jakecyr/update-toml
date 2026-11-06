# Update TOML

A small command-line tool for reading and updating values in TOML files while retaining comments and formatting through [tomlkit](https://github.com/python-poetry/tomlkit).

## Installation

Requires Python 3.10 or later.

```bash
pip install update-toml
```

## Usage

Each command accepts `--file` (`-f`), which defaults to `pyproject.toml`, and a required dot-separated `--path` (`-p`). Keys containing literal dots cannot currently be addressed. Array indexes are not supported.

```bash
# Write a string, including an empty string if needed.
update-toml update --path project.version --value 0.0.1 --file pyproject.toml
update-toml update -p project.description -v ''

# Print a value, or a blank line when the path is missing.
update-toml get --path project.version

# Print True or False. A missing path still exits successfully.
update-toml exists --path project.version
```

`update` always writes a TOML string, even when the argument looks like a number or boolean. It can create the final key but its parent tables must already exist. Root-level keys are supported. Paths with empty segments are invalid. Values returned by `get` are printed using Python's string representation; `get` is primarily intended for scalar values. Use `update-toml --help` or `update-toml COMMAND --help` for options.

Successful commands exit with status 0; file, TOML parsing, and path errors exit with status 1; argument errors exit with status 2. Errors go to stderr. Saving rewrites the file in place; coordinate concurrent writers and keep backups of important files.

## Python API

```python
from update_toml.toml_file import TOMLFile

file = TOMLFile("pyproject.toml")
file.load()
print(file.get_value("project.version"))  # raises KeyError if missing
file.update("project.version", "1.2.3")
file.save()
```

`path_exists` returns a boolean and `get_value_safe` returns `""` for a missing path. All operations require `load()` first. The Python API also accepts TOML-compatible non-string values in `update`.

## Development

Install [Poetry](https://python-poetry.org/docs/#installation), then run:

```bash
poetry install
poetry run pytest
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy update_toml
poetry build
```

The lock file records development and runtime dependencies. To refresh it, run `poetry update` and rerun the checks.
