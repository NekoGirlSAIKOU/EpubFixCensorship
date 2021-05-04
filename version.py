import subprocess

VERSION = subprocess.check_output(['git', 'describe', '--abbrev=0']).decode('ascii').strip()
VERSION = list(int(i) for i in VERSION.replace('v','').split('.'))
VERSION_NAME = subprocess.check_output(['git', 'describe']).decode('ascii').strip()