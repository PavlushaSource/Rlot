import os
import configparser

from lib.utils import get_root_path
from lib.arg_parser.utils import check_ini_file


def get_default_config(mode) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    resources_dir_path = os.path.join(get_root_path(), "resources")

    if mode == "global":
        path_to_default_conf = os.path.join(resources_dir_path, "default_bdev.ini")
    elif mode == "raid":
        path_to_default_conf = os.path.join(resources_dir_path, "default_mdadm.ini")
    else:
        path_to_default_conf = os.path.join(resources_dir_path, "default_spdk.ini")

    check_ini_file(path_to_default_conf)
    config.read(path_to_default_conf)

    return config
