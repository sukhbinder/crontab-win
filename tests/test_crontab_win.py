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
    assert mins == list(range(1, 60))
    assert hour == [8, 10, 11, 12, 13, 14]
    assert day == [28]
    assert month == [9]
    assert dow == [0, 1, 2, 3, 4, 5, 6]
    assert command == ["foo"]


def test_parse_line_empty_command():
    line = "10 14 28 9 3"
    mins, hour, day, month, dow, command = app.parse_line(line)
    assert mins == [10]
    assert hour == [14]
    assert day == [28]
    assert month == [9]
    assert dow == [3]
    assert command == []


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
