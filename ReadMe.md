# EasyBuilder Macro Generator

This is a set of tools to be used in combination with the EasyBuilder Pro app from Weintek.

## What is EasyBuilder Pro?
EasyBuilder Pro is an HMI (Human Machine Interface) designer app that integrates to physical devices sold by Weintek.

## Where does EasyBuilder Macro Generator come in?
This project aims to make integration with other systems easier. Notably, the macro system provided by Weintek lacks some key functionalities and can be a bit tedious to use. So this library attempts to make writing macro code a bit more enjoyable.

## Tools provided
- A python library to allow writing macros in python and generating the resulting macro
- A drawing library for the dynamic drawing object
- A set of tools to import tags from select PLCs (Programmable Logical Computer)

## Usage

First install [python](https://www.python.org/downloads/) (Python 3.9 or newer).

Once installed, make a venv (virtual environment):

Linux:
```sh
python -m venv venv
source ./venv/bin/activate
```

Windows:
```ps
python -m venv venv
.\venv\Scripts\activate
```

Install library:
```sh
python -m pip install --upgrade pip
pip install git+https://github.com/IliTheButterfly/EasyBuilderMacroGenerator.git
```

Then follow the instructions in [Getting started](docs/api/01-getting-started.md).

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
