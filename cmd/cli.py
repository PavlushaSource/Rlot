import sys

from lib import utils
from lib.arg_parser import parser
from lib.logger.bdev_logger import bdev_logger

def main():
    utils.check_fio_exists()
    config = parser.get_config()

    logger = bdev_logger(settings=config)
    logger.generate_fio_file()
    logger.run_fio()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nControl-C pressed")
        sys.exit(1)