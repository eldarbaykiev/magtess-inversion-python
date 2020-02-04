from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic



def show_help(txt):
    help = HelpWindow()
    help.set_message(txt)


    help.exec_()

class HelpWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_helpwindow.ui", self)

        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, 'textBrowser')

        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.close)

    def set_message(self, str):
        self.textBrowser.setPlainText(str)

    def close(self):
        self.accept()
