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
    if "raid" in config and "spdk" in config:
        print(
            "There cannot be [spdk] and [bdev] parameters at the same time!\n")
        sys.exit(2)

    mode = "global"
    if "spdk" in config:
        mode = "spdk"
    elif "raid" in config:
        mode = "raid"

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
        print("The count of bdev in a simple disk test should be equal to 1\n")
        sys.exit(2)

    if mode != "global" and config[mode]["number_realization"] in [0, 1] and len(config[mode]["dev"]) < 2:
        print("The count of bdev in a RAID-0|1 should be equal or grow 2\n")
        sys.exit(2)

    if mode != "global" and config[mode]["number_realization"] == 5 and len(config[mode]["dev"]) < 3:
        print("The count of bdev in a RAID-5 should be equal or grow 3\n")
        sys.exit(2)

    if mode != "global" and config[mode]["number_realization"] == 6 and len(config[mode]["dev"]) < 4:
        print("The count of bdev in a RAID-6 should be equal or grow 4\n")
        sys.exit(2)

    if mode != "global" and int(config[mode]["number_realization"]) not in [0, 1, 5, 6]:
        print(f"RAID-{config[mode]['number_realization']} not support or not exist")
        sys.exit(2)

    if mode == "spdk" and "spdk_json_conf" not in config[mode]:
        print("You must specify the 'spdk_json_conf' parametera\n")
        sys.exit(2)

    return mode






def get_ouput_graphs_path(args):
    if len(args) == 2:
        return painterGraph.get_output_dir_for_graph()
    return args[2]



def main():
    check_ini_file(input())


if __name__ == "__main__":
    main()
