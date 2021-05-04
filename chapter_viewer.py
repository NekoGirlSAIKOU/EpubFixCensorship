from typing import Union
from lxml import etree
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from ChapterViewerWindow import *


class ChapterViewerWindow(QMainWindow):
    def __init__(self, content: Union[str, etree._Element], parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_ChapterViewerWindow()
        self.ui.setupUi(self)

        self.content = content

    @property
    def content(self):
        return self.ui.chapterContent.toHtml()

    @content.setter
    def content(self,value:Union[str,etree._Element]):
        if isinstance(value, str):
            self.ui.chapterContent.setHtml(value)
        else:
            self.ui.chapterContent.setHtml(etree.tounicode(value))
