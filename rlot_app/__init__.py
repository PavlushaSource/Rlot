import sys

from .rlotlib import (
    parseIni,
    checks,
    defaultFio,
    preparationForWork,
    generateFio,
    runFio,
    painterGraph,
)


def draw_graph(path_to_logs):
    painterGraph.draw(path_to_logs)


def get_settings():
    checks.check_args(sys.argv)
    checks.check_ini_file(sys.argv[1])  # check correct input data from filename.ini
    config = parseIni.get_ini_config()
    config = defaultFio.get_default_config(config["global"]["mode"]) | config
    return config


def main():
    checks.check_first()  # fio exist example
    settings_for_fio = get_settings()
    preparationForWork.prepare_env(settings_for_fio)  # run Raid0 or generate Json for Spdk
    fio_path = generateFio.create_fio_file(settings_for_fio)
    runFio.generate_logs(settings_for_fio['output'], settings_for_fio)
    draw_graph(settings_for_fio["output"])
