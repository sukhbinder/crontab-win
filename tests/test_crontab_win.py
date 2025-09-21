from crontab_win import cli
from crontab_win import app
import pytest
from pathlib import Path


def test_create_parser():

    parser = cli.create_parser()
    result = parser.parse_args([])
    assert result.command is None
    assert parser.prog == "crontab"
    assert parser.description == "crontab for windows"


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
