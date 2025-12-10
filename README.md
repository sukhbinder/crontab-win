# crontab-win

[![PyPI](https://img.shields.io/pypi/v/crontab-win.svg)](https://pypi.org/project/crontab-win/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/crontab-win?include_prereleases&label=changelog)](https://github.com/sukhbinder/crontab-win/releases)
[![Tests](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/crontab-win/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/crontab-win/blob/master/LICENSE)

A simple cron-like task scheduler for Windows.

This tool allows you to schedule tasks using a `crontab.txt` file, similar to how cron works on Unix-like systems.

For background on the project read this [blogpost about it](https://sukhbinder.wordpress.com/2025/07/08/introducing-crontab-win/) 

# Installation

Install this tool using `pip`:
```bash
pip install crontab-win
```

# Usage

This package provides two commands: `crontab` and `ctab`. Both can be used interchangeably.

### Running the Scheduler

To start the scheduler, simply run:
```bash
crontab
```
or
```bash
ctab
```
This will start the scheduler in the foreground. It will read your crontab file and execute tasks as per the schedule. You should keep this window minimized.

By default, the scheduler looks for a file named `crontab.txt` in your user's home directory (e.g., `C:\Users\YourUser\crontab.txt`).

You can specify a different crontab file using the `-c` or `--crontab-file` option:
```bash
crontab -c "C:\path\to\my\custom_crontab.txt"
```

### Editing the Crontab File

To open your crontab file for editing, use the `show` command:
```bash
crontab show
```
or
```bash
ctab show
```
This will open `crontab.txt` in your default text editor. If the file doesn't exist, it will be created with a helpful guide.

# Crontab Syntax

Each line in the crontab file represents a single task. The syntax is as follows:

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)
│ │ │ │ │
│ │ │ │ │
* * * * * command to execute
```

You can use `*` for any value, or provide specific numbers. Ranges (`2-5`) and lists (`2,5`) are also supported.

### Special Nicknames

For convenience, you can use the following special nicknames instead of the five-field time specification:

| Nickname      | Equivalent    | Description                               |
|---------------|---------------|-------------------------------------------|
| `@hourly`     | `0 * * * *`   | Run once an hour at the beginning of the hour. |
| `@daily`      | `0 0 * * *`   | Run once a day at midnight.             |
| `@midnight`   | `0 0 * * *`   | (Same as `@daily`)                        |
| `@weekly`     | `0 0 * * 0`   | Run once a week on Sunday midnight.       |
| `@monthly`    | `0 0 1 * *`   | Run once a month on the 1st, at midnight. |
| `@yearly`     | `0 0 1 1 *`   | Run once a year on Jan 1st, at midnight.  |
| `@annually`   | `0 0 1 1 *`   | (Same as `@yearly`)                       |

### Examples

Here are some example crontab entries:

```
# Run a script every 15 minutes
*/15 * * * * python C:\Users\MyUser\scripts\my_script.py

# Run a backup at 5 a.m. every day
0 5 * * * tar -zcf /var/backups/home.tgz /home/

# Use a special nickname to run a task hourly
@hourly echo "This runs every hour" >> C:\temp\hourly.log

# Run a task on the first day of every month
0 0 1 * * echo "Monthly report generation"

# Run a task every Monday at 8:00 AM
0 8 * * MON python C:\path\to\your\script.py
```

# Start Crontab at Startup

To run the crontab scheduler automatically when Windows starts, you can create a simple batch file.

1.  Create a new file named `crontab_startup.bat`.
2.  Add the following content to the file:

    ```cmd
    @echo off
    start /min ctab
    ```

3.  Place this batch file in your startup folder. You can open the startup folder by pressing `Win + R`, typing `shell:startup`, and pressing Enter.

# Development

To contribute to this tool, first check out the code. Then create a new virtual environment:
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
