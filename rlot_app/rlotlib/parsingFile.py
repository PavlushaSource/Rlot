import configparser
import subprocess
import sys
from pathlib import Path




def read_ini_file(filename):
    pass





def main():
    filename = "/resources/raid5.ini"
    config = configparser.ConfigParser()
    config.read(Path(filename))
    print(*config['raid']['dev'].split(','))


if __name__ == "__main__":
    main()
