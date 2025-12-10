import re
import sched
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

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
            lines = [line for line in lines if len(line) != 0]
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
    # unavailable keywords
    REGEX_UNAVAIL = r"(?P<unavail>^@(reboot))"
    match = re.search(REGEX_UNAVAIL, line)
    if match:
        match_unavail = match.group("unavail")
        raise ValueError(f"keyword {match_unavail} is unavailable.")

    # separate schedule-field and command-field
    REGEX = r"(?P<sched>^([0-9a-zA-Z\*\/\,\-]+\s+){4}([0-9a-zA-Z\*\/\,\-]+)|^@(yearly|annually|monthly|weekly|daily|midnight|hourly))(\s*)(?P<cmd>.*)"
    match = re.search(REGEX, line)
    if match:
        sched_str = match.group("sched").lower()
        cmd_str = match.group("cmd")
        sched_str = match.group("sched").lower()
        cmd_str = match.group("cmd")
        if sched_str in ("@yearly", "@annually"):
            sched_str = "0 0 1 1 *"
        elif sched_str == "@monthly":
            sched_str = "0 0 1 * *"
        elif sched_str == "@weekly":
            sched_str = "0 0 * * 0"
        elif sched_str in ("@daily", "@midnight"):
            sched_str = "0 0 * * *"
        elif sched_str == "@hourly":
            sched_str = "0 * * * *"

    else:
        # schedule-field missing
        raise ValueError(f"{line} - schedule-field is not valid.")

    # The name of the months/days into numbers
    name_months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    name_days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

    # if name of the dow range spans the next week
    REGEX_DOW_RANGE = (
        f'(?P<left>.+)(?P<from>{"|".join(name_days)})'
        + f'-(?P<to>{"|".join(name_days)})(?P<right>.+)'
    )
    match = re.search(REGEX_DOW_RANGE, sched_str)
    if match:
        range_to = name_days.index(match.group("to"))
        range_from = name_days.index(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-sat'
            str_to = f'sun-{match.group("to")}'
            if range_from == 6:
                str_from = f"sat"
            if range_to == 0:
                str_to = f"sun"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # if name of the month range spans the next year
    REGEX_MON_RANGE = (
        f'(?P<left>.+)(?P<from>{"|".join(name_months)})'
        + f'-(?P<to>{"|".join(name_months)})(?P<right>.+)'
    )
    match = re.search(REGEX_MON_RANGE, sched_str)
    if match:
        range_to = name_months.index(match.group("to")) + 1
        range_from = name_months.index(match.group("from")) + 1
        if range_from > range_to:
            str_from = f'{match.group("from")}-dec'
            str_to = f'jan-{match.group("to")}'
            if range_from == 12:
                str_from = f"dec"
            if range_to == 1:
                str_to = f"jan"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # name of the dow to numbers
    if any(d in sched_str for d in name_days):
        for idx, d in enumerate(name_days):
            sched_str = sched_str.replace(d, str(idx), 2)

    # name of the month to numbers
    if any(m in sched_str for m in name_months):
        for idx, m in enumerate(name_months):
            sched_str = sched_str.replace(m, str(idx + 1), 2)

    mins, hour, day, month, dow, *_rest = sched_str.split()
    ## if range spans the next period
    # mins
    REGEX_RANGE = r"(?P<left>.*?)(?P<from>[0-9]{1,2})-(?P<to>[0-9]{1,2})(?P<right>.*)"
    match = re.search(REGEX_RANGE, mins)
    if match:
        range_to = int(match.group("to"))
        range_from = int(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-59'
            str_to = f'0-{match.group("to")}'
            if range_from == 59:
                str_from = f"59"
            if range_to == 0:
                str_to = f"0"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # hours
    match = re.search(REGEX_RANGE, hour)
    if match:
        range_to = int(match.group("to"))
        range_from = int(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-23'
            str_to = f'0-{match.group("to")}'
            if range_from == 23:
                str_from = f"23"
            if range_to == 0:
                str_to = f"0"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # day
    match = re.search(REGEX_RANGE, day)
    if match:
        range_to = int(match.group("to"))
        range_from = int(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-31'
            str_to = f'1-{match.group("to")}'
            if range_from == 31:
                str_from = f"31"
            if range_to == 1:
                str_to = f"1"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # month
    match = re.search(REGEX_RANGE, month)
    if match:
        range_to = int(match.group("to"))
        range_from = int(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-12'
            str_to = f'1-{match.group("to")}'
            if range_from == 12:
                str_from = f"12"
            if range_to == 1:
                str_to = f"1"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    # dow
    match = re.search(REGEX_RANGE, dow)
    if match:
        range_to = int(match.group("to"))
        range_from = int(match.group("from"))
        if range_from > range_to:
            str_from = f'{match.group("from")}-6'
            str_to = f'0-{match.group("to")}'
            if range_from == 6:
                str_from = f"6"
            if range_to == 0:
                str_to = f"0"
            raise ValueError(
                f'{match.group("from")}-{match.group("to")} - You cannot set a time span across the multiple periods. {str_from},{str_to} will valid.'
            )

    minutes = list(range(0, 60))  # 0-59
    hours = list(range(0, 24))  # 0-23
    days = list(range(1, 32))  # 1-31
    months = list(range(1, 13))  # 1-12
    dows = list(range(0, 7))  # 0-6

    mins = clean_numbers(mins, minutes)
    hour = clean_numbers(hour, hours)
    day = clean_numbers(day, days)
    month = clean_numbers(month, months)
    dow = clean_numbers(dow, dows)
    return mins, hour, day, month, dow, cmd_str


def get_date():
    return datetime.now()


def run_subprocess(cmdlist):
    si = None
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(
        cmdlist,
        startupinfo=si,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
        text=True,
    )


def process_crontab(crontab_file=None):
    delay = 5
    try:
        lines = get_crontablines(crontab_file)
        date = get_date()
        if lines:
            for line in lines:
                try:
                    mins, hour, day, month, dow, command = parse_line(line)
                except Exception as ex:
                    print(ex, file=sys.stderr)
                    continue
                if date.weekday() in dow:
                    if date.month in month:
                        if date.day in day:
                            if date.hour in hour:
                                if date.minute in mins:
                                    _ = run_subprocess(command)
                                    delay = 60
    except Exception as ex:
        print(ex, file=sys.stderr)
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
    from crontab_win.cli import create_parser

    parser = create_parser()
    main(parser.parse_args())
