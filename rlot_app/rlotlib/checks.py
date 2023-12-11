import os
import shutil
import sys
from . import (
    painterGraph
)

AVAILABLE_GROUP_NAMES = {"global", "raid", "spdk"}
AVAILABLE_PARAMETR_NAMES = {
    "ioengine",
    "invalidate",
    "ramp_time",
    "size",
    "runtime",
    "bs",
    "iodepth",
    "numjobs",
    "rw",
    "dev",
    "number_realization",
    "spdk_json_conf",
}

def check_if_fio_exists():
    command = "fio"
    if shutil.which(command) is None:
        print("Fio executable not found in path. Is Fio installed?\n")
        sys.exit(1)


def define_mode_dev(config):
    mode = "global"
    if "spdk" in config and "raid" not in config:
        mode = "spdk"
    elif "raid" in config and "spdk" not in config:
        mode = "raid"
    elif "raid" in config and "spdk" in config:
        print(
            "There cannot be [spdk] and [bdev] parameters at the same time!\n")
        sys.exit(2)
    return mode


def check_user_config_setting(config):

    for section in config.sections():
        if (section not in AVAILABLE_GROUP_NAMES):
            print(f"incorrect [{section}] section, remove this!\n")
            sys.exit(2)

    mode = define_mode_dev(config)

    for (param, _) in config.items("global"):
        if param not in AVAILABLE_PARAMETR_NAMES:
            print(
                f"Incorrect parameter name - {param}, double-check the configuration file\n")
            sys.exit(2)

    for (param, _) in config.items(mode):
        if param not in AVAILABLE_PARAMETR_NAMES:
            print(
                f"Incorrect parameter name - {param}, double-check the configuration file\n")
            sys.exit(2)

    if "global" not in config:
        print("The [global] is required in the .ini file!\n")
        sys.exit(2)

    if "dev" not in config[mode]:
        print("Dev is a required parameter!\n")
        sys.exit(2)

    if mode != "global" and "number_realization" not in config[mode]:
        print("Number realization parameter is a required!\n")
        sys.exit(2)

    if "rw" not in config["global"]:
        print(
            "Enter the type of testing fio. For example: read, write, randread, randwrite\n")
        sys.exit(2)

    if mode == "spdk" and ("ioengine" not in config["global"] or config["global"]["ioengine"] != "spdk_bdev"):
        print("For spdk testing, the ioengine parameter must be equal to 'spdk_bdev'\n")
        sys.exit(2)

    if mode == "global" and len(config[mode]["dev"].split(',')) != 1:
        print("The number of bdev in a simple disk test should be equal to 1\n")
        sys.exit(2)

    # if mode != "global" and len(config[mode]["dev"])

    if mode == "spdk" and "spdk_json_conf" not in config[mode]:
        print("You must specify the 'spdk_json_conf' parametera\n")
        sys.exit(2)

    return mode


def check_file_extension(filename):

    if (filename.split('.')[-1]) != "ini":
        print("Invalid file extension\n")
        sys.exit(1)


def check_file_exist(filename):

    if not os.path.isfile(filename):
        print(f"Config file {filename} not found\n")
        sys.exit(1)


def check_ini_file(filename):

    check_file_exist(filename)
    check_file_extension(filename)


def get_ouput_graphs_path(args):
    if len(args) == 2:
        return painterGraph.get_output_dir_for_graph()
    return args[2]

def check_args(args):

    if len(args) < 2:
        print("The call failed. Specify the .ini configuration file")
        print("Example: >> python3 rlot.py conf.ini\n")
        sys.exit(1)

    if len(args) > 3:
        print("The call failed. There are too many arguments")
        print("Example: >> python3 rlot.py conf.ini\n")
        sys.exit(1)

    check_ini_file(args[1])


def main():
    check_ini_file(input())


if __name__ == "__main__":
    main()
