import sys

import configparser

from lib.utils import define_mode_dev
from lib.arg_parser.utils import check_args, check_ini_file, check_user_config_setting
from lib.arg_parser.default_configs import get_default_config


def merge_two_conf(old_conf, new_conf):
    for section in new_conf.sections():
        for key, value in new_conf.items(section):
            old_conf[section][key] = value

    return old_conf


def get_ini_config(file_path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    try:
        config.read(file_path)
    except configparser.DuplicateOptionError as err:
        print(f"{err}\n")
        sys.exit(1)

    return config


def get_config() -> configparser.ConfigParser:
    check_args(sys.argv)
    config = get_ini_config(sys.argv[1])
    check_user_config_setting(config)

    # merge default and user config file.ini
    mode = define_mode_dev(config)
    config = merge_two_conf(get_default_config(mode), config)

    return config
