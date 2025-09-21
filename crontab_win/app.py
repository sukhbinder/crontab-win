from random import choice
import sched
import time
from datetime import datetime
import subprocess
from pathlib import Path
import sys

event_schedule = sched.scheduler(time.time, time.sleep)


def process_file(file_path):
    """
    Process a file and return its name and path to an output folder.

    Args:
        file_path (str): The path of the file.

    Returns:
        tuple: A tuple containing the filename and the output folder path.
    """
    return (
        str(Path(file_path).name),
        str(Path(file_path).parent),
    )


def user_crontab(crontab_file=None):
    """Return the directory for user-specific data."""
    if crontab_file:
        return Path(crontab_file)
    return Path.home() / "crontab.txt"


def get_crontablines(crontab_file=None):
    # Path to crontab file
    CRONTABFILE = user_crontab(crontab_file)
    if not CRONTABFILE.exists():
        return None
    else:
        with open(CRONTABFILE, "r") as fin:
            lines = fin.readlines()
            lines = [line.strip() for line in lines if not line.startswith("#")]
        return lines


def clean_numbers(doms, mlist):
    """
    Generate a list of ints that represent the list
    i.e. 2-10,99 -> [2,3,4,5,6,7,8,9,10,99]
    :param doms:
    :return: 'all_doms'' sorted list of  numbers
    """
    if doms == "*":
        clean_doms = mlist
        return clean_doms

    if "*/" in doms:
        inum = int(doms.split("*/")[-1])
        clean_doms = list(range(0, 100, inum))
        clean_doms = list(set(mlist).intersection(clean_doms))
        return clean_doms

    doms = doms.split(",")
    clean_doms = []
    for d in doms:
        if "-" in d:
            w = [int(x) for x in d.split("-")]
            if len(w) != 2:
                raise IOError("Can't parse range {}".format(d))
            else:
                clean_doms += range(min(w), max(w) + 1, 1)
        else:
            clean_doms.append(int(d))
    clean_doms = list(set(mlist).intersection(clean_doms))
    clean_doms.sort()
    return clean_doms


def parse_line(line):
    mins, hour, day, month, dow, *command = line.split()
    minutes = list(range(1, 60))
    hours = list(range(1, 24))
    days = list(range(1, 32))
    months = list(range(1, 13))
    dows = list(range(0, 7))

    mins = clean_numbers(mins, minutes)
    hour = clean_numbers(hour, hours)
    day = clean_numbers(day, days)
    month = clean_numbers(month, months)
    dow = clean_numbers(dow, dows)
    return mins, hour, day, month, dow, command


def get_date():
    return datetime.now()


def run_subprocess(cmdlist):
    si = None
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(
        cmdlist, startupinfo=si, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )


def process_crontab(crontab_file=None):
    delay = 5
    try:
        lines = get_crontablines(crontab_file)
        date = get_date()
        if lines:
            for line in lines:
                mins, hour, day, month, dow, command = parse_line(line)
                if date.weekday() in dow:
                    if date.month in month:
                        if date.day in day:
                            if date.hour in hour:
                                if date.minute in mins:
                                    _ = run_subprocess(command)
                                    delay = 60
    except Exception as ex:
        print(ex)
        pass
    event_schedule.enter(delay, 5, process_crontab, (crontab_file,))


def main(args):
    print("Crontab is active, please keep this minimized")
    if args.crontab_file:
        print(f"To schedule tasks use the {args.crontab_file}")
    else:
        print("To schedule tasks use the crontab.txt in userprofile")
    event_schedule.enter(10, 1, process_crontab, (args.crontab_file,))
    event_schedule.run()


if __name__ == "__main__":
    main()
