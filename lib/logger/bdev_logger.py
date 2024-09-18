from abc import ABC, abstractmethod
from configparser import ConfigParser
import os
import sys
from lib.utils import define_mode_dev, get_current_data, get_root_path, run_command
from .logger import Logger


class Bdev_logger(Logger, ABC):

    def _get_file_name_param(self) -> str:
        return self.settings["global"]["dev"]

    def _get_mode(self) -> str:
        return "bdev"