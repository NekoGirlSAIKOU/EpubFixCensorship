import subprocess

VERSION: str = subprocess.check_output(['git', 'describe', '--abbrev=0']).decode('ascii').strip()
VERSION: tuple = tuple(int(i) for i in VERSION.replace('v', '').split('.'))
VERSION_NAME: str = subprocess.check_output(['git', 'describe']).decode('ascii').strip()
