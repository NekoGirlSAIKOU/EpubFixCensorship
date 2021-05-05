rem git bash is needed.
bash build.sh
mkdir build_windows
mkdir build_windows\languages
mkdir temp
pyinstaller -w -F -n EpubFixCensorship --distpath build_windows --workpath temp build\main.py
copy /Y LICENSE build_windows\LICENSE
copy /Y README.md build_windows\README.md
copy /Y rules.json build_windows\rules.json
copy /Y languages\*.qm build_windows\languages\