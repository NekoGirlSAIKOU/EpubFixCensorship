python build.py
mkdir build_windows
mkdir temp
pyinstaller -w -F -n EpubFixCensorship --distpath build_windows --workpath temp build\main.py
del temp
copy /Y LICENSE build_windows\LICENSE
copy /Y README.md build_windows\README.md
copy /Y rules.json build_windows\rules.json