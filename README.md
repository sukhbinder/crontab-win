crontab-win

[![PyPI](https://img.shields.io/pypi/v/crontab-win.svg)](https://pypi.org/project/crontab-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/crontab-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/crontab-win/releases)
[![Tests](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/crontab-win/blob/master/LICENSE)

# CRONTAB for windows.

Add crontab entries in a textfile and then this programs are executed as per schedule.

To use the crontab.txt, type ``crontab show`` or ``ctab show`` this will open the crontab.txt.

Edit this file to introduce tasks to be run by cron.
 
Each task to run has to be defined through a single line
indicating with different fields when the task will be run
and what command to run for the task

To define the time you can provide concrete values for
minute (m), hour (h), day of month (dom), month (mon),
and day of week (dow) or use '*' in these fields (for 'any').

Notice that tasks will be started based on the system notion of time and timezones.

Output of the crontab jobs (including errors) is shown to the user the crontab file belongs to (unless redirected).

For example, you can run a backup of all your user accounts
at 5 a.m every week with:

```bash
0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
```

Read the [blogpost about it](https://sukhbinder.wordpress.com/2025/07/08/introducing-crontab-win/) 

# Installation

Install this tool using `pip`:
```bash
pip install crontab-win
```
# Usage

For help, run:
```bash
crontab --help
```
You can also use:
```bash
python -m crontab --help
```

# crontab syntax

```bash
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
│ │ │ │ │                                   7 is also Sunday on some systems)
│ │ │ │ │
│ │ │ │ │
* * * * * command to execute
```


# Start crontab at startup
create a batch file 

```cmd
@echo off
start /min ctab 
```

and keep it in ``shell:startup`` folder.



# Development
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
