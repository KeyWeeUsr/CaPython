import sys
from argparse import ArgumentParser, Namespace
from os import environ
from subprocess import Popen


def cmd(*args, **kwargs):
    print(args, kwargs)
    should_skip = False
    if "skip" in kwargs:
        should_skip = kwargs.pop("skip")

    proc = Popen(*args, **kwargs, env=environ)
    proc.communicate()
    if proc.returncode and not should_skip:
        sys.exit(proc.returncode)


def dexec(container, *args):
    cmd(["docker-compose", "exec", container, "sh", "-c", *args])


def get_parser() -> Namespace:
    parser = ArgumentParser()
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    cmd(["docker-compose", "up", "-d"])
    dexec("stdlib", "pip", "install", "-U", "pip")


if __name__ == "__main__":
    main()
