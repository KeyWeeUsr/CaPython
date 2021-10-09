import sys
from os import environ
from os.path import exists, isfile
from subprocess import Popen


def cmd(*args, **kwargs):
    print(args, kwargs)
    proc = Popen(*args, **kwargs)
    proc.communicate()
    if proc.returncode:
        sys.exit(proc.returncode)


def main():
    cmd(["pip", "install", "-U", "pip"])
    cmd(["pip", "install", "camunda-external-task-client-python3"])
    reqs = environ.get("PYTHON_REQUIREMENTS", "/non-existing")
    if exists(reqs) and isfile(reqs):
        cmd(["pip", "install", "-U", "-r", reqs])
    cmd(["python", "-u", "/app/main.py"])


if __name__ == "__main__":
    main()
