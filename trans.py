from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication

trans = QTranslator()

def change_language(file_name:str):
    try :
        trans.load(file_name)
        QApplication.instance().installTranslator(trans)
    except :
        QApplication.instance().removeTranslator(trans)