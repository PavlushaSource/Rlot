from . import (
    checks,
    mdadmGenerate,
)


def run_spdk_prepare_fio(path_to_fio_file):
    return None


def run_default_fio(path_to_fio_file):
    command = ["fio", path_to_fio_file]
    mdadmGenerate.run_command(command)
    
    


def run(path_to_fio_file, settings):
    mode = checks.define_mode_dev(settings)
    if (mode == "spdk"):
        run_spdk_prepare_fio(path_to_fio_file)
    else:
        run_default_fio(path_to_fio_file)