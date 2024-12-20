# crontab-win

[![PyPI](https://img.shields.io/pypi/v/crontab-win.svg)](https://pypi.org/project/crontab-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/crontab-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/crontab-win/releases)
[![Tests](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/crontab-win/blob/master/LICENSE)

crontab for windows. Add crontab entries in a textfile and then this programs are executed as per schedule.

To use this, ``crontab show`` this will open the crontab.txt.
add entry to to it as below

```text
* * * * * notepad
```
This will open notepad every minute

## Installation

Install this tool using `pip`:
```bash
pip install crontab-win
```
## Usage

For help, run:
```bash
crontab --help
```
You can also use:
```bash
python -m crontab --help
```

## crontab syntax

```bash
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * command to execute
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd crontab-win
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
