import subprocess
import sys


NAME_FOR_BDEV = "/dev/md0"
DEVICES_FOR_RAID = ["/dev/sdb", "/dev/sdc", "/dev/sdd", "/dev/sde", "/dev/sdf"]
VERSION_RAID = 0

available_ini_option = {
    "ioengine",
    "invalidate",
    "ramp_time",
    "size",
    "runtime",
    "bs",
    "iodepth",
    "numjobs",
    "mode",
    "rw",
    "dev",
    "number_realization",
}


def run_command(command):
    try:
        result = subprocess.run(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode > 0:
            stdout = result.stdout.decode("UTF-8").strip()
            stderr = result.stderr.decode("UTF-8").strip()
            print(f"\nAn error occurred: stderr: {stderr} - stdout: {stdout} - returncode: {result.returncode} \n")
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(1)
    return result


def mdadm_stop(devices):

    command = ["mdadm"]
    command.append("--stop")
    command.append(NAME_FOR_BDEV)

    run_command(command)

    command = ["mdadm", "--zero-superblock"]
    for dev in devices:
        run_command(command + [dev])

def mdadm_create(devices, version):
    
    create_command = ["mdadm"]
    create_command.append("--create")
    create_command.append("--verbose")
    create_command.append("--chunk=512")
    create_command.append(NAME_FOR_BDEV)
    create_command.append(f"--level={version}")
    create_command.append(f"--raid-devices={len(devices)}")
    for dev in devices:
        create_command.append(dev)

    result = run_command(create_command)
    return result

def main():
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "--create":
        mdadm_create(DEVICES_FOR_RAID, VERSION_RAID)
    elif len(args) > 0 and args[0] == "--stop":
        mdadm_stop(DEVICES_FOR_RAID)
    print("Hello world!")
    

if __name__ == "__main__":
    main()