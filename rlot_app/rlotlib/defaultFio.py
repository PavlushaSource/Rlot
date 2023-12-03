import os
import configparser


def get_default_config(mode):

    config = configparser.ConfigParser()
    if mode == "global":
        path_to_default_conf = get_path_to_resources_dir() + "default_bdev.ini"
    elif mode == "raid":
        path_to_default_conf = get_path_to_resources_dir() + "default_mdadm.ini"
    else:
        path_to_default_conf = get_path_to_resources_dir() + "default_spdk.ini"

    config.read(path_to_default_conf)
    return config


def get_path_to_resources_dir():
    proj_dir = os.path.dirname(os.path.dirname
                               (os.path.dirname(os.path.abspath(__file__))))
    return f"{proj_dir}/resources/"


def main():
    config = get_default_config("raid")
    print(config["raid"]["dev"])


if __name__ == "__main__":
    main()
