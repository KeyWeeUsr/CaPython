import sys
from subprocess import Popen


def cmd(*args, **kwargs):
    should_skip = False
    if "skip" in kwargs:
        should_skip = kwargs.pop("skip")

    proc = Popen(*args, **kwargs)
    proc.communicate()
    if proc.returncode and not should_skip:
        sys.exit(proc.returncode)


def main():
    cmd(["which", "docker"])
    cmd(["docker", "pull", "camunda/camunda-bpm-platform:latest"])
    cmd(["docker", "rm", "-f", "camunda"], skip=True)
    cmd([
        "docker", "run", "-d", "--name", "camunda",
        "-p", "127.0.0.1:8080:8080", "camunda/camunda-bpm-platform:latest"
    ])


if __name__ == "__main__":
    main()
