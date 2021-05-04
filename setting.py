import json
import sys
from typing import Optional

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from SettingWindow import *
from config import PROGRAM_PATH,init_config


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

    def button_apply_clicked(self):
        self.config['element_tags'] = self.ui.lineEdit_element_tags.text().split(' ')
        self.config['element_strings'] = self.ui.lineEdit_element_strings.text().split(' ')
        self.config['check_element_by_rules'] = self.ui.checkBox_check_element_by_rules.isChecked()

        with open ('config.json','w',encoding='utf8') as f:
            json.dump(self.config,f,indent=4,ensure_ascii=False)

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
    setting_window.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())