from crontab_win import cli


def test_create_parser():

    parser = cli.create_parser()
    result = parser.parse_args([])
    assert result.command is None
    assert parser.prog == "crontab"
    assert parser.description == "crontab for windows"
