import sys

from lib import utils
from .consts import AVAILABLE_GROUP_NAMES, AVAILABLE_PARAMETR_NAMES


def check_args(args):
    if len(args) != 2:
        print("The call failed. Specify the .ini configuration file")
        print("Example: >> python3 rlot.py conf.ini\n")
        sys.exit(1)

    check_ini_file(args[1])


def check_file_extension(filename):
    if (filename.split(".")[-1]) != "ini":
        print("Invalid file extension\n")
        sys.exit(1)


def check_ini_file(filename):
    utils.check_file_exist(filename)
    check_file_extension(filename)


def check_user_config_setting(config):
    for section in config.sections():
        if section not in AVAILABLE_GROUP_NAMES:
            print(f"incorrect [{section}] section, remove this!\n")
            sys.exit(2)

    mode = utils.define_mode_dev(config)

    for param, _ in config.items("global"):
        if param not in AVAILABLE_PARAMETR_NAMES:
            print(
                f"Incorrect parameter name - {param}, double-check the configuration file\n"
            )
            sys.exit(2)

    for param, _ in config.items(mode):
        if param not in AVAILABLE_PARAMETR_NAMES:
            print(
                f"Incorrect parameter name - {param}, double-check the configuration file\n"
            )
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
            "Enter the type of testing fio. For example: read, write, randread, randwrite\n"
        )
        sys.exit(2)

    if mode == "spdk" and (
        "ioengine" not in config["global"]
        or config["global"]["ioengine"] != "spdk_bdev"
    ):
        print("For spdk testing, the ioengine parameter must be equal to 'spdk_bdev'\n")
        sys.exit(2)

    if mode == "global" and len(config[mode]["dev"].split(",")) != 1:
        print("The count of bdev in a simple disk test should be equal to 1\n")
        sys.exit(2)

    if (
        mode != "global"
        and config[mode]["number_realization"] in [0, 1]
        and len(config[mode]["dev"]) < 2
    ):
        print("The count of bdev in a RAID-0|1 should be equal or grow 2\n")
        sys.exit(2)

    if (
        mode != "global"
        and config[mode]["number_realization"] == 5
        and len(config[mode]["dev"]) < 3
    ):
        print("The count of bdev in a RAID-5 should be equal or grow 3\n")
        sys.exit(2)

    if (
        mode != "global"
        and config[mode]["number_realization"] == 6
        and len(config[mode]["dev"]) < 4
    ):
        print("The count of bdev in a RAID-6 should be equal or grow 4\n")
        sys.exit(2)

    if mode != "global" and int(config[mode]["number_realization"]) not in [0, 1, 5, 6]:
        print(f"RAID-{config[mode]['number_realization']} not support or not exist")
        sys.exit(2)

    return mode
