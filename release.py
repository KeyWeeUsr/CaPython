import sys
from os import getcwd, remove
from os.path import join, dirname, realpath, exists
from subprocess import Popen

IMAGE_NAME = "keyweeusr/capython"
VERSION = "1.0.0"
TAGS = [
    "3.9.7-slim-buster", "3.9.7-slim-bullseye", "3.9.7-buster",
    "3.9.7-bullseye", "3.9.7-alpine3.14", "3.9.7-alpine3.13",

    "3.8.12-slim-buster", "3.8.12-slim-bullseye", "3.8.12-buster",
    "3.8.12-bullseye", "3.8.12-alpine3.14", "3.8.12-alpine3.13",

    "3.7.12-slim-buster", "3.7.12-slim-bullseye", "3.7.12-buster",
    "3.7.12-bullseye", "3.7.12-alpine3.14", "3.7.12-alpine3.13",

    "3.6.15-slim-buster", "3.6.15-slim-bullseye", "3.6.15-buster",
    "3.6.15-bullseye", "3.6.15-alpine3.14", "3.6.15-alpine3.13",
]


def cmd(*args, **kwargs):
    proc = Popen(*args, **kwargs)
    proc.communicate()
    if proc.returncode:
        sys.exit(proc.returncode)


def main():
    this_folder = dirname(realpath(__file__))
    capy = "capython"
    assert getcwd() == this_folder

    capy_folder = join(this_folder, capy)
    template = join(capy_folder, "Dockerfile.tmpl")
    dest = join(capy_folder, "Dockerfile")

    for tag in TAGS:
        img = f"{IMAGE_NAME}:{VERSION}-{tag}"
        latest = f"{IMAGE_NAME}:{tag}"

        with open(template) as tpl, open(dest, "w") as out:
            out.write(tpl.read().format(tag=tag))

        cmd(["docker", "build", "--tag", img, "capython"], cwd=this_folder)
        cmd(["docker", "tag", img, latest], cwd=this_folder)
        cmd(["docker", "push", img], cwd=this_folder)
        cmd(["docker", "push", latest], cwd=this_folder)

    if exists(dest):
        remove(dest)


if __name__ == "__main__":
    main()
