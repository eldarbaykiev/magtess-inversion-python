# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_Form(object):
    def setupUi(self, Form):
    self.setObjectName("Form")
    self.resize(1075, 84)
    self.progressBar = QtWidgets.QProgressBar(Form)
    self.progressBar.setGeometry(QtCore.QRect(30, 30, 1000, 35))
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
    self.progressBar.setSizePolicy(sizePolicy)
    self.progressBar.setMinimumSize(QtCore.QSize(1000, 35))
    self.progressBar.setMaximumSize(QtCore.QSize(1000, 35))
    self.progressBar.setProperty("value", 0)
    self.progressBar.setObjectName("progressBar")

    self.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)

def retranslateUi(self, Form):
    _translate = QtCore.QCoreApplication.translate
    Form.setWindowTitle(_translate("Form", "Progress bar"))


class ProgressBar(QtWidgets.QDialog, Ui_Form):
    def __init__(self, desc = None, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.setupUi(self)
        self.show()

        if desc != None:
            self.setDescription(desc)

    def setValue(self, val): # Sets value
        self.progressBar.setProperty("value", val)

    def setDescription(self, desc): # Sets Pbar window title
        self.setWindowTitle(desc)

def main():
    app = QtWidgets.QApplication(sys.argv)      # A new instance of QApplication
    form = ProgressBar('pbar')                        # We set the form to be our MainWindow (design)
    app.exec_()                                 # and execute the app

if __name__ == '__main__':                      # if we're running file directly and not importing it
    main()                                      # run the main function

