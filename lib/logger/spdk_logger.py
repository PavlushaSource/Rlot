from abc import ABC, abstractmethod
from configparser import ConfigParser
import json
import os
import sys
from lib.utils import define_mode_dev, get_current_data, get_root_path, run_command
from .logger import Logger


class Spdk_logger(Logger, ABC):
    def __init__(self, settings: ConfigParser, path_to_spdk_repo: str) -> None:
        self.__devices = [i.strip() for i in settings["spdk"]["dev"].split(",")]
        self.__config_spdk_json_path = None
        self.__path_to_spdk_repo = path_to_spdk_repo
        super().__init__(settings)

    def _get_file_name_param(self) -> str:
        return f"SpdkRaid{self.settings['spdk']['number_realization']}"
    def _get_mode(self) -> str:
        return "spdk"

    def generate_spdk_config_json(self) -> None:
        bs_str = self.settings['global']['bs']
        if bs_str[-1] == 'K':
            # convert bs to bytes
            block_size = int(bs_str[:-1]) * 1024
        else:
            print(f"Incorrect block size: {bs_str}")
            sys.exit(1)
        raid_version = self.settings['spdk']['number_realization']

        config = {'subsystems': []}
        config['subsystems'].append({
            'subsystem': 'bdev',
        })
        base_bdevs = []
        config['subsystems'][0]['config'] = []

        for i, dev in enumerate(self.__devices):
            config['subsystems'][0]['config'].append({
                'params': {
                    'block_size': block_size,
                    'filename': dev,
                    'name': f"Uring{i}"
                },
                'method': 'bdev_uring_create'
            })
            base_bdevs.append(f"Uring{i}")

        config['subsystems'][0]['config'].append({
            'method': 'bdev_raid_create',
            'params': {
                'name': self._get_file_name_param(),
                'raid_level': raid_version,
                'strip_size_kb': block_size / 1024,
                'base_bdevs': base_bdevs,
            },
        })

        with open(self.__config_spdk_json_path, 'w') as outfile:
            json.dump(config, outfile)

    def generate_fio_file(self) -> None:
        current_time = get_current_data()
        root_path = get_root_path()
        self._fio_file_path = f"{root_path}/tmp/tmpfile-{current_time}.fio"
        self._logs_dir_path = f"{root_path}/tmp/logs-dir-{current_time}"
        self.__config_spdk_json_path = f"{root_path}/tmp/config-spdk-{current_time}.json"
        os.makedirs(self._logs_dir_path, exist_ok=True)

        self.generate_spdk_config_json()
        fio_config = self._create_config_for_fio(no_value=False)
        fio_config.set("global", "spdk_json_conf", self.__config_spdk_json_path)
        fio_config.set("global", "thread", "1")

        self._write_fio_to_file(fio_config)

    def run_fio(self) -> None:
        preload = f"LD_PRELOAD={self.__path_to_spdk_repo}/build/fio/spdk_bdev"
        command = [preload, "fio", self._fio_file_path]
        run_command(command)
