# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import gmi_pathdialog, gmi_hashdialog, gmi_helpwindow

import sys, os



import gmi_misc

def switch_path(pth):
    old_cwd = os.getcwd()
    try:
        os.chdir(self.GMI_PATH)
    except:
        gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ dr + ', ABORTING...')
    return old_cwd

def switch_path_back(pth):
    os.chdir(pth)
    return








class MainWindow(QtWidgets.QMainWindow):

    GMI_PATH = ''
    GMI_MAGNETIZER = ''
    GMI_TESSBZ = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_mainwindow.ui", self)

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
        HashDialog = gmi_hashdialog.HashDialog()
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

    preselection = gmi_pathdialog.PathDialog()
    if not preselection.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)

    window = MainWindow()

    window.set_path(preselection.GMI_PATH)
    window.read_config()

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
