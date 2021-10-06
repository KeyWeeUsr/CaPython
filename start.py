import sys
from argparse import ArgumentParser, Namespace
from subprocess import Popen


def cmd(*args, **kwargs):
    print(args, kwargs)
    should_skip = False
    if "skip" in kwargs:
        should_skip = kwargs.pop("skip")

    proc = Popen(*args, **kwargs)
    proc.communicate()
    if proc.returncode and not should_skip:
        sys.exit(proc.returncode)


def dexec(container, *args):
    cmd(["docker", "exec", "-it", container, "sh", "-c", *args])


def get_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-s", "--skip-camunda-kill", action="store_true")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    cmd(["which", "docker"])

    camunda_name = "camunda"
    net_name = "camunda-network"
    stdlib_name = "camunda-stdlib"

    cmd(["docker", "network", "create"
    if not args.skip_camunda_kill:
        cmd(["docker", "pull", "camunda/camunda-bpm-platform:latest"])
        cmd(["docker", "rm", "-f", camunda_name], skip=True)
        cmd([
            "docker", "run", "-d",
            "--name", camunda_name,
            "--network", net_name,
            "-p", "127.0.0.1:8080:8080", "camunda/camunda-bpm-platform:latest"
        ])

    cmd(["docker", "rm", "-f", stdlib_name], skip=True)
    cmd([
        "docker", "run", "-d", "--name", stdlib_name,
        "--network", net_name,
        "-p", "127.0.0.1:9090:8080", "python:alpine"
    ])
    dexec(stdlib_name, ["pip", "install", "-U", "pip"])


if __name__ == "__main__":
    main()
