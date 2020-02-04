from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import gmi_pathdialog, gmi_hashdialog, gmi_helpwindow
import gmi_misc

class PathDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_pathdialog.ui", self)

        self.mainlabel = self.findChild(QtWidgets.QLabel, 'mainlabel')
        import datetime
        now = datetime.datetime.now()

        self.mainlabel.setText("Magtess inversion with tesseroids v" + str(0.1) + "\nEldar Baykiev, " + str(now.year))

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

        self.help1 = self.findChild(QtWidgets.QPushButton, 'help1')
        self.help1.clicked.connect(self.help_path)

        self.tessutil_browse = self.findChild(QtWidgets.QPushButton, 'tessutil_browse')
        self.tessutil_browse.clicked.connect(self.get_tessutil)

        self.tessbz_browse = self.findChild(QtWidgets.QPushButton, 'tessbz_browse')
        self.tessbz_browse.clicked.connect(self.get_tessbz)

        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        print(self.buttonBox)
        self.buttonBox.accepted.connect(self.start_main)
        self.buttonBox.rejected.connect(self.reject)

    def help_path(self):
        gmi_helpwindow.show_help('Here you should enter path to your working folder, as well as path to necessary executables from magnetic tesseroids (https://github.com/eldarbaykiev/magnetic-tesseroids).')

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
        #gmi_misc.info(self.GMI_PATH)
        #gmi_misc.info(self.GMI_MAGNETIZER)
        #gmi_misc.info(self.GMI_TESSBZ)
        self.accept()
