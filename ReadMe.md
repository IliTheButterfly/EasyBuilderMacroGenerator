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

First install [python](https://www.python.org/downloads/).

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

## TODO
- [ ] Fix issue with C_IF where variables only used within C_... will not be processed and therefore not added to the variable list
- [ ] Add string to char array conversion
- [ ] Add the rest of the api functions
- [ ] Add recipe generation and management
- [ ] Add structs as a concept that integrates in the code
