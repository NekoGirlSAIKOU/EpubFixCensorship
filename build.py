#!/usr/bin/env python3
# encoding:utf-8
import json
import os
import shutil
import subprocess
import sys


def main():
    try:
        shutil.rmtree('build')
    except FileNotFoundError:
        pass

    try:
        os.makedirs('build')
    except FileExistsError:
        pass

    files = os.listdir()
    for file in files:
        if (file[-3:] == '.py' and file != 'build.py') \
                or file == 'LICENSE' \
                or file == 'README.md' \
                or file == 'requirements.txt'\
                or file == 'rules.json':
            shutil.copy(file, 'build/')

    version_name = subprocess.check_output(['git', 'describe']).decode('ascii').strip()
    version = subprocess.check_output(['git', 'describe', '--abbrev=0']).decode('ascii').strip()
    version = list(int(i) for i in version.replace('v','').split('.'))
    build_info = {
        'version': version,
        'version_name': version_name,
    }
    print('version_name:', build_info['version_name'])
    with open('build/build_info.json', 'w') as f:
        json.dump(build_info, f,indent=4)

    with open ('build/version.py','w') as f:
        f.write(f'VERSION = {version}\n')
        f.write(f'VERSION_NAME = {version_name}\n')


if __name__ == '__main__':
    main()
