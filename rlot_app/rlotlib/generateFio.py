import configparser
import os
import sys
from . import (checks, painterGraph)

def get_output_dir_for_log():
    path = f"/tmp/logs-dir-{painterGraph.get_current_data()}"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def write_fio_file(path, parser):
    try:
        with open(path, 'w') as configfile:
            parser.write(configfile, space_around_delimiters=False)
    except IOError:
        print(f"Failed to write temporary Fio job file at tmpjobfile")
        sys.exit(3)


def create_spdk_fio_file(fio_file):

    return fio_file


def create_fio_file(settings):

    mode = checks.define_mode_dev(settings)
    tmpFioFile = f"/tmp/tmpfile-{painterGraph.get_current_data()}.fio"
    dir_for_log_files = get_output_dir_for_log()
    fio_file = configparser.ConfigParser(allow_no_value=True)

    if mode == "spdk":
        create_spdk_fio_file(fio_file)

    else:
        fio_file["global"] = {}
        fio_file.set("global", "time_based", None)
        for (key, value) in settings.items("global"):
            if key not in ["rw", "dev"]:
                fio_file["global"][key] = value

    for rw in [i.strip() for i in settings["global"]["rw"].split(',')]:
        section_name = f"{rw}-{settings['global']['bs']}"
        fio_file[section_name] = {}
        fio_file[section_name]["filename"] = settings[mode]["dev"]
        fio_file[section_name]["rw"] = rw
        fio_file[section_name]["log_avg_msec"] = "1000"
        fio_file[section_name]["write_bw_log"] = f"{dir_for_log_files}/{settings['global']['bs']}-{rw}-{mode}.results"
        fio_file[section_name]["write_iops_log"] = f"{dir_for_log_files}/{settings['global']['bs']}-{rw}-{mode}.results"
        fio_file[section_name]["write_lat_log"] = f"{dir_for_log_files}/{settings['global']['bs']}-{rw}-{mode}.results"

    print(tmpFioFile)
    write_fio_file(tmpFioFile, fio_file)
    return tmpFioFile, dir_for_log_files
