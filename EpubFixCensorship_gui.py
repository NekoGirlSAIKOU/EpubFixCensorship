#!/usr/bin/env python3
import json
import os
import sys
from typing import Optional, List, Dict, Tuple

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem
from ebooklib import epub
from lxml import etree

from EpubCensorshipFixer import EpubCensorshipFixer
from EpubFixCensorship import set_book_version_metadata
from MainWindow import Ui_MainWindow
from autoreplace import AutoReplace
from chapter_viewer import ChapterViewerWindow
from config import PROGRAM_PATH, init_config
from setting import SettingWindow
from trans import change_language
from version import VERSION_NAME

app: QApplication = ...


class MainWindow(QMainWindow):
    def __init__(self, config: dict, replacer: AutoReplace):
        super().__init__()
        self.config = config

        self.book: Optional[epub.EpubBook] = None
        self.file_name: Optional[str] = None
        self.auto_replacements: List[Tuple[str, str]] = []
        self.current_element_index = 0

        self.replacer = replacer
        self.fixer: EpubCensorshipFixer = ...

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals
        self.ui.actionOpen.triggered.connect(self.open_book_dialog_box)
        self.ui.actionSave.triggered.connect(self.action_save_book)
        self.ui.actionSave_as.triggered.connect(self.save_book_dialog_box)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionAbout.triggered.connect(self.show_about_window)
        self.ui.actionAbout_Qt.triggered.connect(self.show_about_qt)

        self.ui.actionSetting.triggered.connect(self.show_setting_window)

        self.ui.next_button.clicked.connect(self.next)
        self.ui.last_button.clicked.connect(self.last)
        self.ui.add_new_rule.clicked.connect(self.button_add_new_rule_clicked)
        self.ui.show_chapter_button.clicked.connect(self.button_show_chapter_clicked)

        self.ui.reapply_button.clicked.connect(self.button_reapply_clicked)
        self.ui.auto_fix_list.itemDoubleClicked.connect(self.listwidget_item_double_clicked)

    @property
    def current_element(self):
        return self.fixer.censored_element[self.current_element_index]

    @property
    def current_chapter(self):
        return self.fixer.censored_element_chapter[self.current_element_index]

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.book is not None:
            self.ask_will_save()

        with open(f'{PROGRAM_PATH}/rules.json', 'w', encoding='utf8') as f:
            json.dump(self.replacer.rules, f, indent=4, ensure_ascii=False)

        with open(f'{PROGRAM_PATH}/replace_history.json', 'w', encoding='utf8') as f:
            json.dump(self.replacer.replace_histories, f, indent=4, ensure_ascii=False)

        app.exit()



    def open_book(self, file_name):
        self.file_name = file_name
        self.book = epub.read_epub(self.file_name)
        set_book_version_metadata(self.book)

        # clear last book ui
        self.ui.censored_text.clear()
        self.ui.fixed_text.clear()
        self.ui.auto_fix_list.clear()

        # change title
        self.setWindowTitle(f'EpubFixCensorship - {os.path.basename(self.file_name)}')

        # load new book
        self.fixer = EpubCensorshipFixer(self.book, self.replacer,
                                         element_tags=self.config['element_tags'],
                                         element_strings=self.config['element_strings'],
                                         check_element_by_rules=self.config['check_element_by_rules'])
        self.current_element_index = 0
        self.show_element(self.current_element_index)

    def show_element(self, index: int):
        element = self.fixer.censored_element[index]
        element_title = self.fixer.censored_element_chapter_title[index]
        self.ui.chapter_title.setText(element_title)

        origin_text = element.get('censored_text',element.text)

        self.auto_replacements = self.replacer.replace_text(origin_text)

        self.ui.auto_fix_list.clear()
        for replacement in self.auto_replacements:
            self.ui.auto_fix_list.addItem(replacement[0])

        if len(self.auto_replacements)>1:
            self.ui.fixed_text.setPlainText(self.auto_replacements[1][1])
            self.ui.auto_fix_list.setCurrentRow(1)
        else :
            self.ui.fixed_text.setPlainText(element.text)
            self.ui.auto_fix_list.setCurrentRow(-1)
        self.ui.censored_text.setPlainText(self.auto_replacements[0][1])

    def save_fix_result(self, index: int = ...):
        if index is ...:
            index = self.current_element_index
        if self.fixer.censored_element[index].get('censored_text',None) is None:
            self.fixer.censored_element[index].set('censored_text',self.ui.censored_text.toPlainText())
        self.fixer.censored_element[index].text = self.ui.fixed_text.toPlainText()
        self.replacer.replace_histories[self.ui.censored_text.toPlainText()] = self.ui.fixed_text.toPlainText()

    def last(self):
        self.save_fix_result()
        self.current_element_index -= 1
        if self.current_element_index < 0:
            self.current_element_index = 0
            return

        self.show_element(self.current_element_index)

    def next(self):
        self.save_fix_result()
        self.current_element_index += 1
        if self.current_element_index >= len(self.fixer.censored_element):
            self.current_element_index = len(self.fixer.censored_element) - 1
            return

        self.show_element(self.current_element_index)

    def ask_will_save(self):
        # Ask the user if he want to save the epub.
        r = QMessageBox.question(self, self.tr("Question:"), self.tr("Do you want to save current book?"))
        if r == QMessageBox.StandardButton.Yes:
            self.save_book()

    def open_book_dialog_box(self):
        if self.book is not None:
            self.ask_will_save()

        file_name = QFileDialog.getOpenFileName(self, filter='Epub Book (*.epub)')[0]
        if file_name != "":
            self.open_book(file_name)

    def save_book_dialog_box(self):
        if self.book is None:
            return
        file_name = QFileDialog.getSaveFileName(self, filter='Epub Book (*.epub)')[0]
        if file_name != "":
            if not file_name.endswith('.epub'):
                file_name = file_name+'.epub'
            self.file_name = file_name
            self.save_book()

    def action_save_book(self):
        self.save_book()

    def save_book(self, file_name: Optional[str] = None):
        if self.book is None:
            return

        if file_name is None:
            if self.file_name is None:
                return
            file_name = self.file_name

        # Make sure current edit is saved.
        self.save_fix_result()

        self.fixer.regenerate_epub_item()

        epub.write_epub(file_name, self.book)

        # Reset window title
        self.setWindowTitle(f'EpubFixCensorship - {os.path.basename(self.file_name)}')

    def show_about_window(self):
        QMessageBox.about(self, "About:", f"EpubFixCensorship\nVersion:{VERSION_NAME}")

    def show_about_qt(self):
        QMessageBox.aboutQt(self)

    def show_setting_window(self):
        try:
            self.setting_window.close()
        except:
            pass
        self.setting_window = SettingWindow(config=self.config, parent=self)
        self.setting_window.show()

    def button_add_new_rule_clicked(self):
        rule = {
            'pattern': self.ui.new_rule_pattern.text(),
            'replacement': self.ui.new_rule_replacement.text(),
            'isRegex': self.ui.is_regex_rule.isChecked()
        }
        rule['name'] = f'{rule["pattern"]} to {rule["replacement"]}'
        self.ui.new_rule_pattern.setText('')
        self.ui.new_rule_replacement.setText('')
        self.replacer.rules.append(rule)

    def button_show_chapter_clicked(self):
        if self.book is None:
            return
        try:
            self.chapter_viewer_window.close()
        except:
            pass

        old_style = self.current_element.get('style', None)
        if old_style is None:
            self.current_element.set('style', 'color:red')
        else:
            self.current_element.set('style', f'{old_style};color:red')

        content = etree.tounicode(self.current_chapter)
        if old_style is None:
            del self.current_element.attrib['style']
        else:
            self.current_element.set('style', old_style)

        self.chapter_viewer_window = ChapterViewerWindow(content=content, parent=self)
        self.chapter_viewer_window.show()

    def button_reapply_clicked(self):
        self.save_fix_result()
        self.show_element(self.current_element_index)

    def listwidget_item_double_clicked(self, item: QListWidgetItem):
        index = self.ui.auto_fix_list.indexFromItem(item)
        self.ui.fixed_text.setPlainText(self.auto_replacements[index.row()][1])


def main() -> int:
    global app
    app = QApplication(sys.argv)

    # Load config
    try:
        with open(f'{PROGRAM_PATH}/config.json', encoding='utf8') as f:
            config: dict = json.load(f)
    except FileNotFoundError:
        config: dict = {}
    init_config(config)

    # Load rules and history
    try:
        with open(f'{PROGRAM_PATH}/rules.json', encoding='utf8') as f:
            rules: List[dict] = json.load(f)
    except FileNotFoundError:
        rules: List[dict] = []
    try:
        with open(f'{PROGRAM_PATH}/replace_history.json', encoding='utf8') as f:
            replace_history: Dict[str, str] = json.load(f)
    except FileNotFoundError:
        replace_history: Dict[str, str] = {}

    replacer = AutoReplace(rules=rules, replace_histories=replace_history)

    # Load main window
    main_window = MainWindow(config, replacer)

    # Load translation
    change_language(f'{PROGRAM_PATH}/languages/{main_window.config["language"]}.qm')
    main_window.ui.retranslateUi(main_window)

    main_window.show()
    if len(sys.argv) > 1:
        main_window.open_book(file_name=sys.argv[1])
    return app.exec_()


if __name__ == '__main__':
    # Enter main window
    sys.exit(main())
