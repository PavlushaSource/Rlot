import sys
import os

from .rlotlib import (
    parseIni,
    checks,
    defaultFio,
    preparationForWork,
    generateFio,
    runFio,
    painterGraph,
)


def draw_graph(path_to_logs, path_to_graphs_dir, settings):
    painterGraph.draw(path_to_logs, path_to_graphs_dir, settings)


def get_settings():
    checks.check_args(sys.argv)
    # check correct input data from filename.ini
    checks.check_ini_file(sys.argv[1])
    config = parseIni.get_ini_config(sys.argv[1])
    return config


def main():
    checks.check_if_fio_exists()
    settings_for_fio = get_settings()
    settings_for_fio = preparationForWork.prepare_env(settings_for_fio) 
    path_to_fio_file, path_to_log_files = generateFio.create_fio_file(
        settings_for_fio)
    runFio.run(path_to_fio_file, settings_for_fio)
    OUTPUT_GRAPHS_DIRECTORY = checks.get_ouput_graphs_path(sys.argv)
    draw_graph(path_to_log_files, OUTPUT_GRAPHS_DIRECTORY, settings_for_fio)
    preparationForWork.soft_exit(settings_for_fio)


if __name__ == "__main__":
    main()
