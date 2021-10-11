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

    reqs = environ.get("CAPYTHON_REQUIREMENTS", "/non-existing")
    reqs_sep = environ.get("CAPYTHON_REQUIREMENTS_SEPARATOR", ",")
    for req in reqs.split(reqs_sep):
        if not exists(reqs):
            continue
        if not isfile(reqs):
            continue
        cmd(["pip", "install", "-U", "-r", reqs])
    cmd(["python", "-u", "/app/main.py"])


if __name__ == "__main__":
    main()
