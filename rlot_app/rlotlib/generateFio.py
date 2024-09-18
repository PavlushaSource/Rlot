import configparser
import json
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


def generate_raid_config(settings) -> str:
    devices = [i.strip() for i in settings['spdk']['dev'].split(',')]
    bs_str = settings['global']['bs']
    if bs_str[-1] == 'K':
        # convert bs to bytes
        block_size = int(bs_str[:-1]) * 1024
    else:
        print(f"Incorrect block size: {bs_str}")
        sys.exit(1)
    num_blocks = 16
    raid_version = settings['spdk']['number_realization']

    config = {'subsystems': []}
    config['subsystems'].append({
        'subsystem': 'bdev',
    })
    base_bdevs = []
    config['subsystems'][0]['config'] = []


    for i, dev in enumerate(devices):
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
            'name': f"Raid{raid_version}_spdk",
            'raid_level': raid_version,
            'strip_size_kb': block_size / 1024,
            'base_bdevs': base_bdevs,
        },
    })
    
    os.makedirs("out/generated", exist_ok=True)
    filePath = f"out/generated/raid{raid_version}-{block_size}-generated-spdk.json"
    with open(filePath, 'w') as outfile:
        json.dump(config, outfile)
    
    return filePath


def create_spdk_fio_file(fio_file):

    # TODO add spdk_json_conf generate and spdk fio file
    
    return fio_file


def create_fio_file(settings):

    mode = checks.define_mode_dev(settings)
    tmpFioFile = f"/tmp/tmpfile-{painterGraph.get_current_data()}.fio"
    dir_for_log_files = get_output_dir_for_log()
    fio_file = configparser.ConfigParser(allow_no_value=True)

    if mode == "spdk":
        gen_config_path = generate_raid_config(settings)
        
        # create_spdk_fio_file(fio_file)

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
