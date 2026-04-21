# EasyBuilder Macro Generator

This is a set of tools to be used in combination with the EasyBuilder Pro app from Weintek.

## What is EasyBuilder Pro?
EasyBuilder Pro is an HMI (Human Machine Interface) designer app that integrates to physical devices sold by Weintek.

## Where does EasyBuilder Macro Generator come in?
This project aims to make integration with other systems easier. Notably, the macro system provided by Weintek lacks some key functionalities and can be a bit tedious to use. So this library attempts to make writing macro code a bit more enjoyable.

## Tools provided
- A Python library to write macros in Python and generate the resulting EasyBuilder macro code
- A drawing library for the dynamic drawing object
- A set of tools to import and merge tags from select PLCs (Programmable Logic Controllers)

## Installation

First install [Python](https://www.python.org/downloads/) (Python 3.9 or newer).

Once installed, create a virtual environment:

**Linux / macOS:**
```sh
python -m venv venv
source ./venv/bin/activate
```

**Windows:**
```ps
python -m venv venv
.\venv\Scripts\activate
```

Install the library:
```sh
python -m pip install --upgrade pip
pip install git+https://github.com/IliTheButterfly/EasyBuilderMacroGenerator.git
```

Then follow the instructions in [Getting started](docs/api/01-getting-started.md).

## Tag import tools

### CLI tools

| Tool | Description |
|---|---|
| `koyo_tags_import` | Convert a Koyo PLC nicknames CSV to an EasyBuilder tag CSV |
| `combine_tags` | Merge two EasyBuilder tag CSV files into one |

Both tools support `--force`, `--strategy`, and `--dry-run` flags. See their individual docs for details.

### Python API

The same functionality is available as importable functions for use in scripts:

```python
from eb_macro_gen.tools.io import load_eb_tags, save_eb_tags, load_koyo_tags
from eb_macro_gen.tools.merge import merge_eb_tags, ConflictStrategy

# Load and convert Koyo PLC nicknames
koyo_tags = load_koyo_tags("koyo_nicknames.csv", "MyKoyoPLC")

# Merge with existing EasyBuilder tags
existing = load_eb_tags("eb_tags.csv")
merged, result = merge_eb_tags(existing, koyo_tags, strategy=ConflictStrategy.REPLACE_ADDRESS)
print(result)

save_eb_tags(merged, "output.csv")
```

See the [Tags generator docs](docs/api/05-tags-generator.md) for a full end-to-end example including using loaded tags directly in macro generation.

## Running tests

Create and activate a virtual environment (same as the setup instructions above), then install development dependencies and run pytest:

```sh
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

VS Code is preconfigured in `.vscode/settings.json` to run pytest from the repository root with the `src/` layout. Open the Testing panel and click **Run Tests**.

If VS Code shows `No module named pytest`, your selected interpreter is missing test dependencies. Install them in that same environment with `pip install -e ".[dev]"` (or `pip install pytest`).

## TODO
- [ ] Add string to char array conversion
- [ ] Add recipe generation and management
- [ ] Add structs as a concept that integrates in the code
- [ ] Add Rockwell tag import tool