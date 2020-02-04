from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import gmi_pathdialog, gmi_hashdialog, gmi_helpwindow

class HashDialog(QtWidgets.QDialog):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_hashdialog.ui", self)

        self.stage1 = self.findChild(QtWidgets.QLabel, 'stage1')
        self.stage2 = self.findChild(QtWidgets.QLabel, 'stage2')
        self.stage3 = self.findChild(QtWidgets.QLabel, 'stage3')

        self.label_stage1 = self.findChild(QtWidgets.QLabel, 'label_stage1')
        self.label_stage2 = self.findChild(QtWidgets.QLabel, 'label_stage2')
        self.label_stage3 = self.findChild(QtWidgets.QLabel, 'label_stage3')

        self.button_close = self.findChild(QtWidgets.QPushButton, 'button_close')
        self.button_close.clicked.connect(self.close)

    def set_path(self, wpath):
        self.GMI_PATH = wpath
        print(self.GMI_PATH)

    def close(self):
        self.accept()

    def check(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.stage1.setPixmap(pixmap)
        self.stage1.show()
        self.stage2.setPixmap(pixmap)
        self.stage2.show()
        self.stage3.setPixmap(pixmap)
        self.stage3.show()

        import gmi_hash_test
        stages = [0, 0, 0]
        stages, dict = gmi_hash_test.main(self.GMI_PATH)

        pixmap_checked =  QtGui.QPixmap('icons/icons8-checked-checkbox-40.png')
        pixmap_unchecked =  QtGui.QPixmap('icons/icons8-unchecked-checkbox-40.png')

        if stages[0] > 0:
            self.stage1.setPixmap(pixmap_checked)
            self.label_stage1.setText('correct checksum')
        elif stages[0] == 0:
            self.stage1.setPixmap(pixmap_unchecked)
            self.label_stage1.setText('no checksum')
        else:
            self.stage1.setPixmap(pixmap_unchecked)
            self.label_stage1.setText('checksum in dictionary\ndoes not match')
        self.stage1.show()

        if stages[1] > 0:
            self.stage2.setPixmap(pixmap_checked)
            self.label_stage2.setText('correct checksum')
        elif stages[0] == 0:
            self.stage2.setPixmap(pixmap_unchecked)
            self.label_stage2.setText('no checksum')
        else:
            self.stage2.setPixmap(pixmap_unchecked)
            self.label_stage2.setText('checksum in dictionary\ndoes not match')
        self.stage2.show()

        if stages[2] > 0:
            self.stage3.setPixmap(pixmap_checked)
            self.label_stage3.setText('correct checksum')
        elif stages[0] == 0:
            self.stage3.setPixmap(pixmap_unchecked)
            self.label_stage3.setText('no checksum')
        else:
            self.stage3.setPixmap(pixmap_unchecked)
            self.label_stage3.setText('checksum in dictionary\ndoes not match')
        self.stage3.show()
