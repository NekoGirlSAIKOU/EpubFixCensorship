python build.py
mkdir build_windows
mkdir temp
pyinstaller -w -F -n EpubFixCensorship --distpath build_windows --workpath temp build/main.py
del temp