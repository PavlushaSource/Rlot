import sys

from lib import utils
from lib.arg_parser import parser
from lib.logger.mdadm_logger import Mdadm_logger
from lib.logger.bdev_logger import Bdev_logger
from lib.logger.spdk_logger import Spdk_logger

def main():
    utils.check_fio_exists()
    config = parser.get_config()

    logger = Spdk_logger(settings=config, path_to_spdk_repo="/root/spdk")
    logger.generate_fio_file()
    logger.run_fio()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nControl-C pressed")
        sys.exit(1)
