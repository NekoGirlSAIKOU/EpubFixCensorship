# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName("SettingWindow")
        SettingWindow.resize(799, 345)
        self.centralwidget = QtWidgets.QWidget(SettingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_element_tags = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_element_tags.setObjectName("lineEdit_element_tags")
        self.horizontalLayout_2.addWidget(self.lineEdit_element_tags)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_element_strings = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_element_strings.setObjectName("lineEdit_element_strings")
        self.horizontalLayout_3.addWidget(self.lineEdit_element_strings)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.checkBox_check_element_by_rules = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_check_element_by_rules.setObjectName("checkBox_check_element_by_rules")
        self.verticalLayout.addWidget(self.checkBox_check_element_by_rules)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.button_ok = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ok.sizePolicy().hasHeightForWidth())
        self.button_ok.setSizePolicy(sizePolicy)
        self.button_ok.setObjectName("button_ok")
        self.horizontalLayout_4.addWidget(self.button_ok)
        self.button_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout_4.addWidget(self.button_cancel)
        self.button_apply = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_apply.sizePolicy().hasHeightForWidth())
        self.button_apply.setSizePolicy(sizePolicy)
        self.button_apply.setObjectName("button_apply")
        self.horizontalLayout_4.addWidget(self.button_apply)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        SettingWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 23))
        self.menubar.setObjectName("menubar")
        SettingWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingWindow)
        self.statusbar.setObjectName("statusbar")
        SettingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SettingWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingWindow.setWindowTitle(_translate("SettingWindow", "Setting"))
        self.label.setText(_translate("SettingWindow", "Check elements with these tags:"))
        self.label_2.setText(_translate("SettingWindow", "Check elements containing these strings:"))
        self.checkBox_check_element_by_rules.setText(_translate("SettingWindow", "Check elements that can be processed by rules(May decrease performance)"))
        self.button_ok.setText(_translate("SettingWindow", "OK"))
        self.button_cancel.setText(_translate("SettingWindow", "Cancel"))
        self.button_apply.setText(_translate("SettingWindow", "Apply"))
