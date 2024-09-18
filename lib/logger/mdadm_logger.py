from abc import ABC
from configparser import ConfigParser
from .logger import Logger

from lib.utils import run_command

class Mdadm_logger(Logger, ABC):
    def __init__(self, settings: ConfigParser) -> None:
        self.__devices = [i.strip() for i in settings["raid"]["dev"].split(",")]
        super().__init__(settings)


    def _get_file_name_param(self) -> str:
        return f"dev/md_{self.settings['raid']['number_realization']}"

    def _get_mode(self) -> str:
        return "mdadm"

    def __create_mdadm_init_command(self) -> list[str]:
        command_init = ["mdadm"]
        command_init.append("--create")
        command_init.append("--verbose")
        command_init.append("--chunk=512")
        command_init.append(self._get_file_name_param())
        command_init.append(f"--level={self.settings["raid"]["number_realization"]}")

        command_init.append(f"--raid-devices={len(self.__devices)}")
        for x in self.__devices:
            command_init.append(x)

        return command_init

    def start_logger(self) -> None:
    
        command = self.__create_mdadm_init_command()
        print("Start logger", command)
        run_command(command)

        self.settings['raid']['dev'] = self._get_file_name_param()


    def free_logger(self) -> None:
        command = ["mdadm"]
        command.append("--stop")
        command.append(self._get_file_name_param())
        run_command(command)

        command = ["mdadm", "--zero-superblock"]
        for dev in self.__devices:
            run_command(command + [dev])
