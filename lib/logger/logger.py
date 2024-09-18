from abc import ABC, abstractmethod
from configparser import ConfigParser
import os
import sys
from lib.utils import define_mode_dev, get_current_data, get_root_path, run_command


class Logger(ABC):

    @abstractmethod
    def _get_file_name_param(self) -> str: ...

    @abstractmethod
    def _get_mode(self) -> str: ...

    def __init__(self, settings: ConfigParser) -> None:
        self.settings = settings
        self.__fio_file_path = None
        self.__logs_dir_path = None

    def start_logger(self) -> None:
        pass

    def free_logger(self) -> None:
        pass

    def __create_config_for_fio(self) -> ConfigParser:
        fio_file = ConfigParser(allow_no_value=True)
        file_name_param = self._get_file_name_param()

        fio_file["global"] = {}
        fio_file.set("global", "time_based", None)
        for key, value in self.settings.items("global"):
            if key not in ["rw", "dev"]:
                fio_file["global"][key] = value

        for rw in [i.strip() for i in self.settings["global"]["rw"].split(",")]:
            section_name = f"{rw}-{self.settings['global']['bs']}"
            fio_file[section_name] = {}
            fio_file[section_name]["filename"] = file_name_param
            fio_file[section_name]["rw"] = rw

            # TODO think about log_avg_msec
            fio_file[section_name]["log_avg_msec"] = "1000"

            mode = self._get_mode()
            fio_file[section_name][
                "write_bw_log"
            ] = f"{self.__logs_dir_path}/{self.settings['global']['bs']}-{rw}-{mode}.results"
            fio_file[section_name][
                "write_iops_log"
            ] = f"{self.__logs_dir_path}/{self.settings['global']['bs']}-{rw}-{mode}.results"
            fio_file[section_name][
                "write_lat_log"
            ] = f"{self.__logs_dir_path}/{self.settings['global']['bs']}-{rw}-{mode}.results"

        return fio_file

    def __write_fio_to_file(self, fio_config: ConfigParser) -> None:
        try:
            with open(self.__fio_file_path, "w") as fio_file:
                fio_config.write(fio_file, space_around_delimiters=False)
        except IOError:
            print(f"Failed to write temporary Fio job file at tmpjobfile")
            sys.exit(3)

    def generate_fio_file(self) -> None:
        current_time = get_current_data()
        root_path = get_root_path()
        self.__fio_file_path = f"{root_path}/tmp/tmpfile-{current_time}.fio"
        self.__logs_dir_path = f"{root_path}/tmp/logs-dir-{current_time}"
        os.makedirs(self.__logs_dir_path, exist_ok=True)

        fio_config = self.__create_config_for_fio()
        self.__write_fio_to_file(fio_config)

    def run_fio(self) -> None:
        command = ["fio", self.__fio_file_path]
        run_command(command)
