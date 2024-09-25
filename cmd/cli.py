import sys

from lib import utils
from lib.arg_parser import parser
from lib.logger.mdadm_logger import Mdadm_logger
from lib.logger.bdev_logger import Bdev_logger
from lib.logger.spdk_logger import Spdk_logger
from lib.logger.logger import Logger
from lib.utils import define_mode_dev
from lib.drawer.painter import Painter

def main():
    utils.check_fio_exists()
    config = parser.get_config()

    mode = define_mode_dev(config)

    logger: Logger = None
    if mode == "global":
        logger = Bdev_logger(settings=config)
    elif mode == "raid":
        logger = Mdadm_logger(settings=config)
    else:
        logger = Spdk_logger(settings=config)

    logger.start_logger()
    logger.generate_fio_file()
    logger.run_fio()
    logger.free_logger()

    painter = Painter(logger._logs_dir_path, config, logger._get_mode(), logger._get_file_name_param())
    painter.draw_graph()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nControl-C pressed")
        sys.exit(1)
