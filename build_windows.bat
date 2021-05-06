@rem git bash is needed.

bash build.sh
mkdir build_windows
mkdir build_windows\languages
mkdir temp

@rem Patch for pyinstaller
echo= >> build\config.py
echo import sys >> build\config.py
echo PROGRAM_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0] >> build\config.py

pyinstaller -w -F -n EpubFixCensorship_gui --distpath build_windows --workpath temp build\EpubFixCensorship_gui.py
pyinstaller -c -F -n EpubFixCensorship --distpath build_windows --workpath temp build\EpubFixCensorship.py
copy /Y LICENSE build_windows\LICENSE
copy /Y README.md build_windows\README.md
copy /Y rules.json build_windows\rules.json
copy /Y languages\*.qm build_windows\languages\