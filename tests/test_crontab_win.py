from crontab_win import cli
from crontab_win import app
import pytest
from pathlib import Path
import unittest.mock as mock
import datetime
import subprocess


def test_create_parser():

    parser = cli.create_parser()
    result = parser.parse_args([])
    assert result.command is None
    assert parser.prog == "crontab"
    assert parser.description == "Crontab for windows"


def test_process_file():
    a, b = app.process_file(__file__)
    assert b == str(Path(__file__).parent)
    assert a == "test_crontab_win.py"

    a, b = app.process_file("test_crontab_win.py")
    assert b == r"."
    assert a == "test_crontab_win.py"


def test_parse_line():
    line = "* 8,10-14 28 9 * foo"

    mins, hour, day, month, dow, command = app.parse_line(line)
    assert mins == list(range(0, 60)) # 0-59
    assert hour == [8, 10, 11, 12, 13, 14]
    assert day == [28]
    assert month == [9]
    assert dow == [0, 1, 2, 3, 4, 5, 6]
    assert command == "foo"


def test_parse_line_contain_spaces_cmd():
    line = "* 8,10-14 28 9 * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line)
    assert mins == list(range(0, 60)) # 0-59
    assert hour == [8, 10, 11, 12, 13, 14]
    assert day == [28]
    assert month == [9]
    assert dow == [0, 1, 2, 3, 4, 5, 6]
    assert command == "cmd.exe /c \"echo test...\""


def test_parse_line_mins_range():
    line00    = "00 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line01    = "01 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line58    = "58 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line59    = "59 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line60    = "60 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line00_27 = "00-27 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line27_59 = "27-59 8,10-14 28 9 * cmd.exe /c \"echo test...\""
    line59_60 = "59-60 8,10-14 28 9 * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line00)
    assert mins == [0]

    mins, hour, day, month, dow, command = app.parse_line(line01)
    assert mins == [1]

    mins, hour, day, month, dow, command = app.parse_line(line58)
    assert mins == [58]

    mins, hour, day, month, dow, command = app.parse_line(line59)
    assert mins == [59]

    mins, hour, day, month, dow, command = app.parse_line(line60)
    assert mins == []

    mins, hour, day, month, dow, command = app.parse_line(line00_27)
    assert mins == list(range(0, 28)) # 0-27

    mins, hour, day, month, dow, command = app.parse_line(line27_59)
    assert mins == list(range(27, 60)) # 0-59

    mins, hour, day, month, dow, command = app.parse_line(line59_60)
    assert mins == [59]


def test_parse_line_hours_range():
    line00    = "0 0  28 9 * cmd.exe /c \"echo test...\""
    line01    = "0 1  28 9 * cmd.exe /c \"echo test...\""
    line22    = "0 22 28 9 * cmd.exe /c \"echo test...\""
    line23    = "0 23 28 9 * cmd.exe /c \"echo test...\""
    line24    = "0 24 28 9 * cmd.exe /c \"echo test...\""
    line00_03_20_23 = "0 0-3,20-23 28 9 * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line00)
    assert hour == [0]

    mins, hour, day, month, dow, command = app.parse_line(line01)
    assert hour == [1]

    mins, hour, day, month, dow, command = app.parse_line(line22)
    assert hour == [22]

    mins, hour, day, month, dow, command = app.parse_line(line23)
    assert hour == [23]

    mins, hour, day, month, dow, command = app.parse_line(line24)
    assert hour == []

    mins, hour, day, month, dow, command = app.parse_line(line00_03_20_23)
    assert hour == [0, 1, 2, 3, 20, 21, 22, 23]


def test_parse_line_days_range():
    line00    = "0 0 00 9 * cmd.exe /c \"echo test...\""
    line01    = "0 0 01 9 * cmd.exe /c \"echo test...\""
    line30    = "0 0 30 9 * cmd.exe /c \"echo test...\""
    line31    = "0 0 31 9 * cmd.exe /c \"echo test...\""
    line32    = "0 0 32 9 * cmd.exe /c \"echo test...\""
    line00_03_20_32 = "0 0 0-3,20-32 9 * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line00)
    assert day == []

    mins, hour, day, month, dow, command = app.parse_line(line01)
    assert day == [1]

    mins, hour, day, month, dow, command = app.parse_line(line30)
    assert day == [30]

    mins, hour, day, month, dow, command = app.parse_line(line31)
    assert day == [31]

    mins, hour, day, month, dow, command = app.parse_line(line32)
    assert day == []

    mins, hour, day, month, dow, command = app.parse_line(line00_03_20_32)
    assert day == [1, 2, 3, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


def test_parse_line_month_range():
    line00    = "0 0 01 0  * cmd.exe /c \"echo test...\""
    line01    = "0 0 01 1  * cmd.exe /c \"echo test...\""
    line02    = "0 0 01 2  * cmd.exe /c \"echo test...\""
    line11    = "0 0 01 11 * cmd.exe /c \"echo test...\""
    line12    = "0 0 01 12 * cmd.exe /c \"echo test...\""
    line13    = "0 0 01 13 * cmd.exe /c \"echo test...\""
    line00_03_11_13 = "0 0 01 0-3,11-13 * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line00)
    assert month == []

    mins, hour, day, month, dow, command = app.parse_line(line01)
    assert month == [1]

    mins, hour, day, month, dow, command = app.parse_line(line02)
    assert month == [2]

    mins, hour, day, month, dow, command = app.parse_line(line11)
    assert month == [11]

    mins, hour, day, month, dow, command = app.parse_line(line12)
    assert month == [12]

    mins, hour, day, month, dow, command = app.parse_line(line13)
    assert month == []

    mins, hour, day, month, dow, command = app.parse_line(line00_03_11_13)
    assert month == [1, 2, 3, 11, 12]


def test_parse_line_name_dow():
    line_sun = "0 0 01 jan sun cmd.exe /c \"echo test...\""
    line_mon = "0 0 01 feb mon cmd.exe /c \"echo test...\""
    line_tue = "0 0 01 mar tue cmd.exe /c \"echo test...\""
    line_wed = "0 0 01 apr wed cmd.exe /c \"echo test...\""
    line_thu = "0 0 01 may thu cmd.exe /c \"echo test...\""
    line_fri = "0 0 01 jun fri cmd.exe /c \"echo test...\""
    line_sat = "0 0 01 jul sat cmd.exe /c \"echo test...\""
    line_mon_fri         = "0 0 01 aug mon-fri cmd.exe /c \"echo test...\""
    line_mon_tue_thu_sun = "0 0 01 sep mon,tue,thu-sun cmd.exe /c \"echo test...\""
    line_wed_sat_tue     = "0 0 01 9 wed,sat-tue cmd.exe /c \"echo test...\""
    #line_wed_sat_tue     = "0 0 01 9 3,6-6,0-2 cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line_sun)
    assert dow == [0]

    mins, hour, day, month, dow, command = app.parse_line(line_mon)
    assert dow == [1]

    mins, hour, day, month, dow, command = app.parse_line(line_tue)
    assert dow == [2]

    mins, hour, day, month, dow, command = app.parse_line(line_wed)
    assert dow == [3]

    mins, hour, day, month, dow, command = app.parse_line(line_thu)
    assert dow == [4]

    mins, hour, day, month, dow, command = app.parse_line(line_fri)
    assert dow == [5]

    mins, hour, day, month, dow, command = app.parse_line(line_sat)
    assert dow == [6]

    mins, hour, day, month, dow, command = app.parse_line(line_mon_fri)
    assert dow == [1,2,3,4,5]

    mins, hour, day, month, dow, command = app.parse_line(line_mon_tue_thu_sun)
    assert dow == [0,1,2,4,5,6]

    mins, hour, day, month, dow, command = app.parse_line(line_wed_sat_tue)
    assert dow == [0,1,2,3,6]


def test_parse_line_name_month():
    line_jan = "0 0 01 jan * cmd.exe /c \"echo test...\""
    line_feb = "0 0 01 feb * cmd.exe /c \"echo test...\""
    line_mar = "0 0 01 mar * cmd.exe /c \"echo test...\""
    line_apr = "0 0 01 apr * cmd.exe /c \"echo test...\""
    line_may = "0 0 01 may * cmd.exe /c \"echo test...\""
    line_jun = "0 0 01 jun * cmd.exe /c \"echo test...\""
    line_jul = "0 0 01 jul * cmd.exe /c \"echo test...\""
    line_aug = "0 0 01 aug * cmd.exe /c \"echo test...\""
    line_sep = "0 0 01 sep * cmd.exe /c \"echo test...\""
    line_oct = "0 0 01 oct * cmd.exe /c \"echo test...\""
    line_nov = "0 0 01 nov * cmd.exe /c \"echo test...\""
    line_dec = "0 0 01 dec * cmd.exe /c \"echo test...\""
    line_jan_dec   = "0 0 01 jan-dec * cmd.exe /c \"echo test...\""
    line_janfebmar = "0 0 01 jan,feb,mar * cmd.exe /c \"echo test...\""
    line_janfebmar_oct_dec = "0 0 01 jan,feb,mar,oct-dec * cmd.exe /c \"echo test...\""
    line_janfebmar_aug_oct_feb = "0 0 01 aug,oct-feb * cmd.exe /c \"echo test...\""

    mins, hour, day, month, dow, command = app.parse_line(line_jan)
    assert month == [1]

    mins, hour, day, month, dow, command = app.parse_line(line_feb)
    assert month == [2]

    mins, hour, day, month, dow, command = app.parse_line(line_mar)
    assert month == [3]

    mins, hour, day, month, dow, command = app.parse_line(line_apr)
    assert month == [4]

    mins, hour, day, month, dow, command = app.parse_line(line_may)
    assert month == [5]

    mins, hour, day, month, dow, command = app.parse_line(line_jun)
    assert month == [6]

    mins, hour, day, month, dow, command = app.parse_line(line_jul)
    assert month == [7]

    mins, hour, day, month, dow, command = app.parse_line(line_aug)
    assert month == [8]

    mins, hour, day, month, dow, command = app.parse_line(line_sep)
    assert month == [9]

    mins, hour, day, month, dow, command = app.parse_line(line_oct)
    assert month == [10]

    mins, hour, day, month, dow, command = app.parse_line(line_nov)
    assert month == [11]

    mins, hour, day, month, dow, command = app.parse_line(line_dec)
    assert month == [12]

    mins, hour, day, month, dow, command = app.parse_line(line_janfebmar)
    assert month == [1,2,3]

    mins, hour, day, month, dow, command = app.parse_line(line_janfebmar_oct_dec)
    assert month == [1,2,3,10,11,12]

    mins, hour, day, month, dow, command = app.parse_line(line_janfebmar_aug_oct_feb)
    assert month == [1,2,8,10,11,12]


def test_parse_line_empty_command():
    line = "10 14 28 9 3"
    mins, hour, day, month, dow, command = app.parse_line(line)
    assert mins == [10]
    assert hour == [14]
    assert day == [28]
    assert month == [9]
    assert dow == [3]
    assert command == ""


def test_parse_line_invalid_input():
    with pytest.raises(ValueError):
        app.parse_line("a b c d e")


def test_clean_numbers():
    assert app.clean_numbers("*", list(range(1, 60))) == list(range(1, 60))
    assert app.clean_numbers("*/2", list(range(0, 100, 2))) == list(range(0, 100, 2))
    assert app.clean_numbers("2-10,99", list(range(1, 100))) == [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        99,
    ]
    assert app.clean_numbers("2-10", list(range(1, 100))) == list(range(2, 11))
    assert app.clean_numbers("1,3,5", list(range(1, 10))) == [1, 3, 5]


def test_clean_numbers_invalid_range():
    with pytest.raises(ValueError):
        app.clean_numbers("5+2", list(range(1, 10)))


def test_get_crontablines(tmpdir):
    crontab_file = tmpdir / "crontab.txt"
    crontab_file.write("1 2 3 4 5 command\n# comment\n6 7 8 9 10 another command")
    lines = app.get_crontablines(crontab_file)
    assert lines == ["1 2 3 4 5 command", "6 7 8 9 10 another command"]


def test_user_crontab():
    assert app.user_crontab("test.txt") == Path("test.txt")
    assert app.user_crontab() == Path.home() / "crontab.txt"