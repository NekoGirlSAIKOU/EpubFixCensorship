#!/usr/bin/env python3
# encoding:utf-8
import json
import os
import shutil
import subprocess
from config import PROGRAM_PATH
import sys

def main():
    try:
        shutil.rmtree(f'{PROGRAM_PATH}/build')
    except FileNotFoundError:
        pass

    try:
        os.makedirs(f'{PROGRAM_PATH}/build')
    except FileExistsError:
        pass

    if sys.platform == 'win32':
        subprocess.check_output(f'bash {PROGRAM_PATH}/UpdateUI.sh')
    else:
        subprocess.check_output(f'{PROGRAM_PATH}/UpdateUI.sh')

    files = os.listdir(PROGRAM_PATH)
    for file in files:
        if (file[-3:] == '.py' and file != 'build.py') \
                or file == 'LICENSE' \
                or file == 'README.md' \
                or file == 'requirements.txt'\
                or file == 'rules.json':
            shutil.copy(f'{PROGRAM_PATH}/{file}', f'{PROGRAM_PATH}/build/')

    version_name = subprocess.check_output(['git', 'describe']).decode('ascii').strip()
    version = subprocess.check_output(['git', 'describe', '--abbrev=0']).decode('ascii').strip()
    version = tuple(int(i) for i in version.replace('v','').split('.'))
    build_info = {
        'version': version,
        'version_name': version_name,
    }
    print('version_name:', build_info['version_name'])
    with open(f'{PROGRAM_PATH}/build/build_info.json', 'w') as f:
        json.dump(build_info, f,indent=4)

    with open (f'{PROGRAM_PATH}/build/version.py','w') as f:
        f.write(f'VERSION = {version}\n')
        f.write(f'VERSION_NAME = "{version_name}"\n')


if __name__ == '__main__':
    main()
