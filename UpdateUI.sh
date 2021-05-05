#!/usr/bin/env sh
# UI
pyuic5 MainWindow.ui -o MainWindow.py
pyuic5 SettingWindow.ui -o SettingWindow.py
pyuic5 ChapterViewerWindow.ui -o ChapterViewerWindow.py

# Translation
pylupdate5 *.py -ts languages/zh-CN.ts