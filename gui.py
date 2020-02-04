# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import sys, os

import gmi_misc



class Dialog(QtWidgets.QDialog):



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("dialog.ui", self)

        self.mainlabel = self.findChild(QtWidgets.QLabel, 'mainlabel')
        #self.mainlabel.setText("Hello World!")

        self.GMI_PATH = '/Volumes/Seagate Backup Plus Drive 1/python3_inv_mutiplicator'
        self.gmi_path = self.findChild(QtWidgets.QLineEdit, 'gmi_path')
        self.gmi_path.setText(self.GMI_PATH)

        self.GMI_MAGNETIZER = '/Volumes/Seagate Backup Plus Drive 1/python3_inv_mutiplicator/tessutil_magnetize_model'
        self.gmi_tessutil_filename = self.findChild(QtWidgets.QLineEdit, 'gmi_tessutil_filename')
        self.gmi_tessutil_filename.setText(self.GMI_MAGNETIZER)

        self.GMI_TESSBZ = '/Volumes/Seagate Backup Plus Drive 1/python3_inv_mutiplicator/tessbz'
        self.gmi_tessbz_filename = self.findChild(QtWidgets.QLineEdit, 'gmi_tessbz_filename')
        self.gmi_tessbz_filename.setText(self.GMI_TESSBZ)


        self.path_browse = self.findChild(QtWidgets.QPushButton, 'path_browse')
        self.path_browse.clicked.connect(self.get_path)

        self.tessutil_browse = self.findChild(QtWidgets.QPushButton, 'tessutil_browse')
        self.tessutil_browse.clicked.connect(self.get_tessutil)

        self.tessbz_browse = self.findChild(QtWidgets.QPushButton, 'tessbz_browse')
        self.tessbz_browse.clicked.connect(self.get_tessbz)

        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        print(self.buttonBox)
        self.buttonBox.accepted.connect(self.start_main)
        self.buttonBox.rejected.connect(self.reject)


    def get_path(self):
        fdialog = QtWidgets.QFileDialog()
        fdialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        #fdialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, false);
        fdialog.exec()
        pname = fdialog.directory().absolutePath()
        print(pname)
        self.gmi_path.setText(pname)
        self.GMI_PATH = str(pname)


    def get_tessutil(self):
        fname, typ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Executable (*)")
        self.gmi_tessutil_filename.setText(fname)
        self.GMI_MAGNETIZER = fname

    def get_tessbz(self):
        fname, typ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Executable (*)")
        self.gmi_tessbz_filename.setText(fname)
        self.GMI_TESSBZ = fname

    def start_main(self):

        gmi_misc.info(self.GMI_PATH)
        gmi_misc.info(self.GMI_MAGNETIZER)
        gmi_misc.info(self.GMI_TESSBZ)
        self.accept()

class Hashtest(QtWidgets.QDialog):

    GMI_PATH = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("hashtest.ui", self)

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



class MainWindow(QtWidgets.QMainWindow):

    GMI_PATH = ''
    GMI_MAGNETIZER = ''
    GMI_TESSBZ = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)

        self.config_editor = self.findChild(QtWidgets.QTextEdit, 'config_editor')

        self.button_save = self.findChild(QtWidgets.QPushButton, 'button_save')
        self.button_save.clicked.connect(self.save_config)

        self.button_check = self.findChild(QtWidgets.QPushButton, 'button_checksum')
        self.button_check.clicked.connect(self.check_hashtest)

        self.button_close = self.findChild(QtWidgets.QPushButton, 'button_close')
        self.button_close.clicked.connect(self.close)

        self.button_observed = self.findChild(QtWidgets.QPushButton, 'button_observed')
        self.button_observed.clicked.connect(self.plot_observed)


    def set_path(self, wpath):
        self.GMI_PATH = wpath
        print(self.GMI_PATH)

    def read_config(self):
        with open(self.GMI_PATH + '/input.txt', 'r') as config_file:
            buf = config_file.read()
            self.config_editor.setText(buf)

    def save_config(self):
        buf = self.config_editor.toPlainText()
        with open(self.GMI_PATH + '/input.txt', 'w') as config_file:
            config_file.write(buf)

        self.read_config()
        gmi_misc.info('Config file was saved!')

    def check_hashtest(self):
        HashDialog = Hashtest()
        HashDialog.set_path(self.GMI_PATH)

        HashDialog.show()
        HashDialog.check()

        HashDialog.exec_()
        #HashDialog.loop()

    def plot_observed(self):
        old_cwd = os.getcwd()
        try:
            os.chdir(self.GMI_PATH)
        except:
            gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ dr + ', ABORTING...')

        import gmi_gmt

        import matplotlib.pyplot as plt

        import gmi_config
        gmi_config.read_config()

        try:
        	raw_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.OBSERVED_DATA)
        	#raw_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.OBSERVED_DATA)
        	raw_grid = raw_grid
        except IOError as err:
        	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
        	exit(-1)

        gmi_gmt.plot_global_grid(raw_grid, 'Observed Field', -12, 12, 'polar', 'Magnetic field', 'nT')

        os.chdir(old_cwd)

    def close(self):
        exit(0)





def main():
    app = QtWidgets.QApplication(sys.argv)

    preselection = Dialog()
    if not preselection.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)

    window = MainWindow()

    window.set_path(preselection.GMI_PATH)
    window.read_config()

    window.show()

    sys.exit(app.exec_())

main()
