import json
import os
import sys
from typing import Optional
from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from SettingWindow import *
from config import PROGRAM_PATH,init_config
from trans import change_language


class SettingWindow(QMainWindow):
    def __init__(self,config:dict,parent:Optional[QMainWindow]=None):
        super().__init__(parent=parent)

        self.config = config

        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)


        self.ui.lineEdit_element_tags.setText(' '.join(config['element_tags']))
        self.ui.lineEdit_element_strings.setText(' '.join(config['element_strings']))
        self.ui.checkBox_check_element_by_rules.setChecked(config['check_element_by_rules'])

        self.ui.button_apply.clicked.connect(self.button_apply_clicked)
        self.ui.button_ok.clicked.connect(self.button_ok_clicked)
        self.ui.button_cancel.clicked.connect(self.button_cancel_clicked)

        files = os.listdir(f'{PROGRAM_PATH}/languages')
        for file in files:
            if file.endswith('.qm'):
                self.ui.comboBox_language.addItem(file[0:-3])
        self.ui.comboBox_language.addItem('eng')

    def button_apply_clicked(self):
        self.config['element_tags'] = self.ui.lineEdit_element_tags.text().split(' ')
        self.config['element_strings'] = self.ui.lineEdit_element_strings.text().split(' ')
        self.config['check_element_by_rules'] = self.ui.checkBox_check_element_by_rules.isChecked()
        self.config["language"] = self.ui.comboBox_language.currentText()
        with open ('config.json','w',encoding='utf8') as f:
            json.dump(self.config,f,indent=4,ensure_ascii=False)

        # Load translation
        change_language(f'{PROGRAM_PATH}/languages/{self.config["language"]}.qm')
        self.ui.retranslateUi(self)
        try :
            self.parent().ui.retranslateUi(self.parent())
        except:
            pass

    def button_ok_clicked(self):
        self.button_apply_clicked()
        self.close()

    def button_cancel_clicked(self):
        self.close()


def main():
    try:
        with open(f'{PROGRAM_PATH}/config.json') as f:
            config: dict = json.load(f)
    except FileNotFoundError:
        config: dict = {}
    init_config(config)

    app = QApplication(sys.argv)
    setting_window = SettingWindow(config)

    # Load translation
    change_language(f'{PROGRAM_PATH}/languages/{setting_window.config["language"]}.qm')
    setting_window.ui.retranslateUi(setting_window)

    setting_window.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())