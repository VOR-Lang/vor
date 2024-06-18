import os
import sys
import subprocess


def cwd():
    print(os.getcwd())


def ls():
    print(os.listdir(os.getcwd()))


def cd(path):
    os.chdir(path)


def run(command):
    subprocess.run(command, shell=True)


def join(*args):
    return os.path.join(*args)


def read(file):
    with open(file, "r") as f:
        print(f.read())


def write(file, content):
    with open(file, "w") as f:
        f.write(content)


def append(file, content):
    with open(file, "a") as f:
        f.write(content)


def remove(file):
    os.remove(file)


def mkdir(path):
    os.mkdir(path)


def rmdir(path):
    os.rmdir(path)


def touch(file):
    with open(file, "w") as f:
        pass


def whoami():
    print(os.getlogin())


def exit(code=0):
    code = int(code)
    sys.exit(code)


def zip(file, path):
    run(f"zip -r {file} {path}")
