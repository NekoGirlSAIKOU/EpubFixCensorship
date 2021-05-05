#!/usr/bin/env python3
# encoding:utf-8
import json
import os
import shutil
import subprocess
from config import PROGRAM_PATH
import sys

def main():
    try :
        save_path = sys.argv[1]
    except IndexError:
        save_path = f'{PROGRAM_PATH}/build/version.py'


    version_name = subprocess.check_output(['git', 'describe']).decode('ascii').strip()
    version = subprocess.check_output(['git', 'describe', '--abbrev=0']).decode('ascii').strip()
    version = tuple(int(i) for i in version.replace('v','').split('.'))

    print('version_name:', version_name)

    with open (save_path,'w') as f:
        f.write(f'VERSION = {version}\n')
        f.write(f'VERSION_NAME = "{version_name}"\n')


if __name__ == '__main__':
    main()
