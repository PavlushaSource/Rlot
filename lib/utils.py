from datetime import datetime
import os
import shutil
import subprocess
import sys


def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_file_exist(filename):
    if not os.path.isfile(filename):
        print(f"Config file {filename} not found\n")
        sys.exit(1)


def check_fio_exists():
    command = "fio"
    if shutil.which(command) is None:
        print("Fio executable not found in path. Is Fio installed?\n")
        sys.exit(1)


def define_mode_dev(config):
    if "raid" in config and "spdk" in config:
        print("There cannot be [spdk] and [bdev] parameters at the same time!\n")
        sys.exit(2)

    mode = "global"
    if "spdk" in config:
        mode = "spdk"
    elif "raid" in config:
        mode = "raid"

    return mode


def get_current_data():
    return datetime.now().strftime("%d-%m-%Y-%H-%M-%S")


def get_current_data_short():
    return datetime.now().strftime("%d/%m/%Y")


def run_command(command, my_env=None) -> None:
    try:
        result = subprocess.run(
            command,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=my_env,
        )
        stdout = result.stdout.decode("UTF-8").strip()
        print(stdout)
        if result.returncode > 0:  # run Raid0 or generate Json for Spdkrncode > 0:
            stderr = result.stderr.decode("UTF-8").strip()
            print(
                f"\nAn error occurred: stderr: {stderr} - stdout: {stdout} - returncode: {result.returncode} \n"
            )
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(1)
