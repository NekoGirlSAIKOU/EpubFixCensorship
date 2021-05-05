#!/usr/bin/env sh
echo Remove old build
rm -r build

echo Update UI
./UpdateUI.sh

echo Copy files to build dir
mkdir build
mkdir build/languages
cp *.py build/
rm build/generate_version.py
cp rules.json build/
cp LICENSE build/
cp README.md build/
cp requirements.txt build/
cp -r languages/*.qm build/languages/

echo execute generate_version.py
python generate_version.py build/version.py

echo Build finished.


