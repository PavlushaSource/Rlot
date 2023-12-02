
import sys
import configparser


def get_bdev_default_config():
    config = {}
    config["ioengine"] = "libaio"
    config["invalidate"] = 1
    config["ramp_time"] = 5
    config["size"] = None
    config["dev"] = None
    config["iodepth"] = 32
    config["numjobs"] = 8
    config["runtime"] = 60
    config["bs"] = "4k"
    config["mode"] = "bdev"
    config["rw"] = ["write", "read"]
    return config

def get_raid_default_config():
    config = {}
    return config
    
    

def get_default_config(mode):
    if mode == "bdev":
        config = get_bdev_default_config()
    elif mode == "raid":
        config = get_raid_default_config()
    else:
        print("Mode={mode} is node defined")
        sys.exit(3)
    return config


def main():
    config = get_bdev_default_config()
    custom_config = configparser.ConfigParser()
    custom_config.read("/root/Rlot/resources/bdev.ini")
    config |= custom_config["global"]
    print(config)
    
    
if __name__ == "__main__":
    main()