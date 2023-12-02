import shutil
import sys
from MdadmGenerate import available_ini_option


def check_if_fio_exists():
    command = "fio"
    if shutil.which(command) is None:
        print("Fio executable not found in path. Is Fio installed?\n")
        sys.exit(1)


def check_fio_setting(settings):
    if settings["type"] not in ["device"]:
        print("\nType should be a device for Rlot correct work.\n")
        sys.exit(2)

    mode_available = ["spdk", "raid", "bdev"]
    if settings["global"]["mode"]:
        print("hello blin")


def check_first():
    return None


def check_ini_file(filename):
    check_file_exist(filename)
    return None


def check_file_exist(filename):
    return None


def check_args(args):
    return None
