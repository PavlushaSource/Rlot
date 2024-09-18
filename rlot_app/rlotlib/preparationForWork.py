from . import (mdadmGenerate, checks)


def prepare_env(settings):
    mode = checks.define_mode_dev(settings)
    dev = [i.strip() for i in settings[mode]['dev'].split(',')]
    if mode == 'raid':
        mdadmGenerate.mdadm_create(dev, settings[mode]["number_realization"])
        settings[mode]["dev"] = mdadmGenerate.NAME_FOR_BDEV
    return settings

def soft_exit(settings):
    mode = checks.define_mode_dev(settings)
    dev = [i.strip() for i in settings[mode].split(',')]
    if mode == 'raid':
        mdadmGenerate.mdadm_stop(dev)



