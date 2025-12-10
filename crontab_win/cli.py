import argparse

import os
import sys

from crontab_win.app import user_crontab, main

TEXT = """# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12) OR jan,feb,mar,apr ...
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │                                   OR sun,mon,tue,wed,thu,fri,sat
# │ │ │ │ │
# * * * * * command to execute"""


def create_parser():
    parser = argparse.ArgumentParser(prog="crontab", description="Crontab for windows")
    parser.add_argument(
        "-c",
        "--crontab-file",
        type=str,
        default=None,
        help="Specify a crontab file with full path.",
    )

    subparsers = parser.add_subparsers(dest="command", required=False)

    run_parser = subparsers.add_parser("run", help="Main run parser")
    run_parser.set_defaults(func=mainrun)

    show_parser = subparsers.add_parser("show", help="Shows the ``crontab.txt`` ")
    show_parser.set_defaults(func=showcrontab)

    parser.set_defaults(func=mainrun)

    return parser


def cli():
    "crontab for windows"
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


def showcrontab(args):
    crontab_path = user_crontab(args.crontab_file)
    # Check if file exists
    if not crontab_path.exists():
        crontab_path.touch()
        crontab_path.write_text(TEXT)

    prog = "cmd /c start" if sys.platform == "win32" else "open"
    try:
        _ = os.system(f"{prog} \"{str(crontab_path)}\"")
    except FileNotFoundError:
        print("File does not exist. ")


def mainrun(args):
    main(args)