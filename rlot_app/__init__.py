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
    config = parseIni.get_ini_config(sys.argv[1])
    return config


def main():
    checks.check_if_fio_exists()  # fio exists
    settings_for_fio = get_settings()
    # preparationForWork.prepare_env(settings_for_fio)  # run Raid0 or generate Json for Spdk
    generateFio.create_fio_file(settings_for_fio)
    # runFio.generate_logs(settings_for_fio['output'], settings_for_fio)
    # draw_graph(settings_for_fio["output"])

if __name__ == "__main__":
    main()