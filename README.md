# crontab-win

[![PyPI](https://img.shields.io/pypi/v/crontab-win.svg)](https://pypi.org/project/crontab-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/crontab-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/crontab-win/releases)
[![Tests](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/crontab-win/blob/master/LICENSE)

crontab for windows

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
