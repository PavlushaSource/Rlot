import configparser
import subprocess
import sys
from pathlib import Path


def run_raw_command(command, outputfile=None):
    try:
        result = subprocess.run(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode > 0 or (len(str(result.stderr)) > 3):
            stdout = result.stdout.decode("UTF-8").strip()
            stderr = result.stderr.decode("UTF-8").strip()
            print(f"\nAn error occurred: stderr: {stderr} - stdout: {stdout} - returncode: {result.returncode} \n")
            sys.exit(result.returncode)
    except KeyboardInterrupt:
        print(f"\n ctrl-c pressed - Aborted by user....\n")
        sys.exit(1)
    return result


def read_ini_file(filename):
    pass


def main():
    filename = "/home/pavlusha/Documents/PracticeWork/Rlot/resources/raid5.ini"
    config = configparser.ConfigParser()
    config.read(Path(filename))
    print(*config['raid']['dev'].split(','))


if __name__ == "__main__":
    main()
