# Update TOML

Simple CLI to update a value in a TOML file.

## Installation

Install with pip:

```bash
pip install update-toml
```

## Usage

### Update

Run the following command, passing in a path and value to update in the specified .toml file:

```bash
update-toml update --path project.version --value 0.0.1 --file pyproject.toml
```

### Get

Get a value from a .toml file:

```bash
update-toml get --path project.version --file pyproject.toml
# Example return: 0.0.1
```

### Exists

Check if a path exists in a .toml file:

```bash
update-toml exists --path project.version --file pyproject.toml
# Example return: True or False
```
