from random import choice
import sched
import time
from datetime import datetime
import subprocess
from pathlib import Path
import sys

event_schedule = sched.scheduler(time.time, time.sleep)


def user_crontab():
    """Return the directory for user-specific data."""
    return Path.home() / "crontab.txt"


def get_crontablines():
    # Path to crontab file
    CRONTABFILE = user_crontab()
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


def process_crontab():
    delay = 5
    try:
        lines = get_crontablines()
        date = get_date()
        for line in lines:
            print(line)
            mins, hour, day, month, dow, command = parse_line(line)
            if date.weekday() in dow:
                if date.month in month:
                    if date.day in day:
                        if date.hour in hour:
                            if date.minute in mins:
                                iret = run_subprocess(command)
                                delay = 60
    except Exception as ex:
        print(ex)
        pass
    event_schedule.enter(delay, 5, process_crontab, ())


def main():
    print("Crontab is active, please keep this minimized")
    print("To schedule tasks use the crontab.txt in userprofile")
    event_schedule.enter(10, 1, process_crontab, ())
    event_schedule.run()


if __name__ == "__main__":
    main()
