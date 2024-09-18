import sys

from ...lib.arg_parser import default_configs
from . import (
    checks,
)

import configparser

def merge_two_conf(old_conf, new_conf):
    for section in new_conf.sections():
        for (key, value) in new_conf.items(section):
            old_conf[section][key] = value

    return old_conf

def get_ini_config(file_path):
    config = configparser.ConfigParser()

    try:
        config.read(file_path)
    except configparser.DuplicateOptionError as err:
        print(f"{err}\n")
        sys.exit(1)

    checks.check_user_config_setting(config)
    config = merge_two_conf(default_configs.get_default_config(checks.define_mode_dev(config)), config)
    return config