import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="crontab for windows")
    parser.add_argument("name", type=str, help="Dummy argument")
    return parser


def cli():
    "crontab for windows"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    print(args)