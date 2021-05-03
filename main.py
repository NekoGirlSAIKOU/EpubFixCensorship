import json
import sys
from typing import Optional, List, Tuple, Dict

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox, QProgressDialog, \
    QListWidgetItem
from ebooklib import epub
import ebooklib
from lxml import etree
import os
from MainWindow import *
from autoreplace import AutoReplace

VERSION = (0, 1, 0)
VERSION_NAME = '.'.join(str(i) for i in VERSION)
app: QApplication = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.book: Optional[epub.EpubBook] = None
        self.file_name: Optional[str] = None
        self.chapters: List[epub.EpubHtml] = []
        self.current_chapter_index = 0
        self.current_chapter: Optional[etree._Element] = None
        self.chapter_elements: List[etree._Element] = []
        self.current_element_index = 0

        self.auto_replacements:List[Tuple[str,str]]=[]

        try :
            with open ('rules.json') as f:
                self.rules:List[dict] = json.load(f)
        except FileNotFoundError:
            self.rules:List[dict] = []

        try :
            with open ('replace_history.json') as f:
                self.replace_history:Dict[str,str] = json.load(f)
        except FileNotFoundError:
            self.replace_history:Dict[str,str]={}

        self.replacer = AutoReplace(rules=self.rules,replace_histories=self.replace_history)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self.open_book_dialog_box)
        self.ui.actionSave.triggered.connect(self.save_book)
        self.ui.actionSave_as.triggered.connect(self.save_book_dialog_box)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionAbout.triggered.connect(self.show_about_window)
        self.ui.actionAbout_Qt.triggered.connect(self.show_about_qt)

        self.ui.next_button.clicked.connect(self.next_element)
        self.ui.last_button.clicked.connect(self.last_element)
        self.ui.add_new_rule.clicked.connect(self.button_add_new_rule_clicked)

        self.ui.reapply_button.clicked.connect(self.button_reapply_clicked)
        self.ui.auto_fix_list.itemDoubleClicked.connect(self.listwidget_item_double_clicked)

    def closeEvent(self, QCloseEvent):
        if self.book is not None:
            self.ask_will_save()

        with open ('rules.json','w') as f:
            json.dump(self.rules,f,indent=4,ensure_ascii=False)

        with open ('replace_history.json','w') as f:
            json.dump(self.replace_history,f,indent=4,ensure_ascii=False)

        app.exit()

    def open_book_dialog_box(self):
        if self.book is not None:
            self.ask_will_save()

        file_name = QFileDialog.getOpenFileName()[0]
        if file_name != "":
            self.open_book(file_name)

    def open_book(self, file_name):
        self.file_name = file_name
        self.book = epub.read_epub(self.file_name)
        self.book.set_unique_metadata(None, 'meta', '', {'name': 'EpubFixCensorship version', 'content': VERSION_NAME})

        # clear last book ui
        self.ui.censored_text.clear()
        self.ui.fixed_text.clear()
        self.ui.auto_fix_list.clear()

        # clear last book cache
        self.chapters.clear()
        self.current_chapter_index = -1
        self.current_chapter = None
        self.chapter_elements.clear()
        self.current_element_index = 0

        # change title
        self.setWindowTitle(f'EpubFixCensorship - {os.path.basename(self.file_name)}')

        # load new book
        self.chapters = list(self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        self.next_chapter()

    def save_book_dialog_box(self):
        file_name = QFileDialog.getSaveFileName()[0]
        if file_name != "":
            self.file_name = file_name
            self.save_book()

    def save_book(self, file_name: Optional[str] = None):
        if self.book is None:
            return

        if file_name is None:
            if self.file_name is None:
                return
            file_name = self.file_name


        # Make sure current edit is saved.
        self.save_current_element()
        self.save_current_chapter()

        epub.write_epub(file_name, self.book)

    def show_about_window(self):
        QMessageBox.about(self, "About:", f"EpubFixCensorship\nVersion:{VERSION_NAME}")

    def show_about_qt(self):
        QMessageBox.aboutQt(self)

    def ask_will_save(self):
        # Ask the user if he want to save the epub.
        r = QMessageBox.question(self, "Do you want to save", "Do you want to save current book?")
        if r == QMessageBox.StandardButton.Yes:
            self.save_book()

    def last_element(self):
        self.save_current_element()
        if self.current_element_index <= 0:
            # There is no more element
            # Last chapter
            self.last_chapter()
        else:
            # Next element
            self.current_element_index -= 1
            self.show_element()

    def next_element(self):
        self.save_current_element()
        if self.current_element_index >= len(self.chapter_elements) - 1:
            # There is no more element
            # Next chapter
            self.next_chapter()
        else:
            # Next element
            self.current_element_index += 1
            self.show_element()

    def save_current_element(self):
        try :
            current_element = self.chapter_elements[self.current_element_index]
            if current_element.get('censored_text') is None:
                current_element.set('censored_text',current_element.text)
            current_element.text = self.ui.fixed_text.toPlainText()

            if current_element.text != current_element.get('censored_text'):
                self.replace_history[current_element.get('censored_text')] = current_element.text
        except IndexError:
            pass

    def show_element(self,original_text = None):
        try :
            current_element = self.chapter_elements[self.current_element_index]
        except:
            return
        if original_text is None:
            original_text = current_element.get("censored_text",current_element.text)

        self.ui.auto_fix_list.clear()
        self.ui.censored_text.setPlainText(original_text)

        self.auto_replacements = self.replacer.replace_text(original_text)
        try :
            # index 0 is origin result
            self.ui.fixed_text.setPlainText(self.auto_replacements[1][1])
        except IndexError:
            self.ui.fixed_text.setPlainText(current_element.text)
        for replacement in self.auto_replacements:
            self.ui.auto_fix_list.addItem(replacement[0])
        try :
            self.ui.chapter_title.setText(self.current_chapter.xpath('/html/head/title//text()')[0])
        except IndexError:
            self.ui.chapter_title.setText('')

    def last_chapter(self):
        self.save_current_chapter()
        if self.current_chapter_index <= 0:
            # There is no more chapter
            QMessageBox.information(self, "Information", "This is the last chapter")
            return
        else:
            self.current_chapter_index -= 1
            self.current_chapter: etree._Element = etree.HTML(
                self.chapters[self.current_chapter_index].content)
            self.chapter_elements = self.filter_element(self.current_chapter.cssselect('p,div'))
            if self.chapter_elements == []:
                return self.last_chapter()
            self.current_element_index = len(self.chapter_elements)-1

            self.show_element()

    def next_chapter(self):
        self.save_current_chapter()

        if self.current_chapter_index >= len(self.chapters) - 1:
            # There is no more chapter
            QMessageBox.information(self, "Information", "There is no more chapter")
            return
        else:
            self.current_chapter_index += 1
            self.current_chapter: etree._Element = etree.HTML(
                self.chapters[self.current_chapter_index].content)
            self.chapter_elements = self.filter_element(self.current_chapter.cssselect('p,div'))
            if self.chapter_elements == []:
                return self.next_chapter()
            self.current_element_index = 0

            self.show_element()

    def filter_element(self,elements:List[etree._Element])->List[etree._Element]:
        r:List[etree._Element] = []
        for element in elements:
            if element.text is None:
                continue
            elif '*' not in element.get('censored_text',element.text):
                continue
            r.append(element)
        return r

    def save_current_chapter(self):
        if self.current_chapter is not None:
            self.chapters[self.current_chapter_index].content = etree.tounicode(self.current_chapter)

    def button_reapply_clicked(self):
        self.save_current_element()
        self.show_element(original_text=self.ui.fixed_text.toPlainText())

    def button_add_new_rule_clicked(self):
        rule = {
            'pattern':self.ui.new_rule_pattern.text(),
            'replacement':self.ui.new_rule_replacement.text(),
            'isRegex':self.ui.is_regex_rule.isChecked()
        }
        rule['name'] = f'{rule["pattern"]} to {rule["replacement"]}'
        self.ui.new_rule_pattern.setText('')
        self.ui.new_rule_replacement.setText('')
        self.rules.append(rule)

    def listwidget_item_double_clicked(self,item:QListWidgetItem):
        index = self.ui.auto_fix_list.indexFromItem(item)
        self.ui.fixed_text.setPlainText(self.auto_replacements[index.row()][1])


def main() -> int:
    global app
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    return app.exec_()


if __name__ == '__main__':
    exit(main())
