import sys
from os import environ
from subprocess import Popen  # noqa


def cmd(*args, **kwargs):
    print(args, kwargs)
    should_skip = False
    if "skip" in kwargs:
        should_skip = kwargs.pop("skip")

    with Popen(*args, **kwargs, env=environ) as proc:  # noqa
        proc.communicate()
        if proc.returncode and not should_skip:
            sys.exit(proc.returncode)


def dexec(container, *args):
    cmd(["docker-compose", "exec", container, "sh", "-c", *args])


def main():
    cmd(["docker-compose", "up", "-d"])


if __name__ == "__main__":
    main()
