from .logger import Logger


class Bdev_logger(Logger):
    def _get_file_name_param(self) -> str:
        return self.settings["global"]["dev"]

    def _get_mode(self) -> str:
        return "bdev"
