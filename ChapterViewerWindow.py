# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChapterViewerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChapterViewerWindow(object):
    def setupUi(self, ChapterViewerWindow):
        ChapterViewerWindow.setObjectName("ChapterViewerWindow")
        ChapterViewerWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ChapterViewerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.chapterContent = QtWidgets.QTextEdit(self.centralwidget)
        self.chapterContent.setReadOnly(True)
        self.chapterContent.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.chapterContent.setObjectName("chapterContent")
        self.verticalLayout.addWidget(self.chapterContent)
        ChapterViewerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ChapterViewerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        ChapterViewerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ChapterViewerWindow)
        self.statusbar.setObjectName("statusbar")
        ChapterViewerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ChapterViewerWindow)
        QtCore.QMetaObject.connectSlotsByName(ChapterViewerWindow)

    def retranslateUi(self, ChapterViewerWindow):
        _translate = QtCore.QCoreApplication.translate
        ChapterViewerWindow.setWindowTitle(_translate("ChapterViewerWindow", "Chapter Viewer"))

