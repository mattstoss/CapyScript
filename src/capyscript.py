import sys
from lib import runner


def main(args):
    if len(args) < 1:
        raise ValueError("usage: python capyscript.py [FILEPATH]")
    filepath = args[0]
    runner.execute_file(filepath)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
