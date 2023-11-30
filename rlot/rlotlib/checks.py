import shutil
import sys


def check_if_fio_exists():
    command = "fio"
    if shutil.which(command) is None:
        print("Fio executable not found in path. Is Fio installed?\n")
        sys.exit(1)


def check_fio_setting(settings):
    if settings["type"] not in ["device"]:
        print("\nType should be a device for Rlot correct work.\n")
        sys.exit(2)

    if settings["mode"] not in ["write", "randwrite", "read", "randread"]:
        print("\nMode should be one of the options: [write, randwrite, read, randread].\n")
        sys.exit(3)

