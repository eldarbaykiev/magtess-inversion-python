from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import gmi_pathdialog, gmi_helpwindow
import gmi_misc
import configparser
import os
import shutil
import stat


class PathDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_pathdialog.ui", self)

        self.setModal(True)

        if not os.path.isfile(".config.ini"):
            self.cfg = configparser.ConfigParser()
            self.cfg['PATH'] = {'GMI_PATH' : '',
                              'GMI_MAGNETIZER' : '',
                              'GMI_TESSBX' : '',
                              'GMI_TESSBY' : '',
                              'GMI_TESSBZ' : ''}
            with open('.config.ini', 'w') as configfile:
                self.cfg.write(configfile)


        self.setFixedSize(QtCore.QSize(self.width(), self.height()))

        self.cfg = configparser.ConfigParser()
        #with open('.config.ini', 'r') as configfile:
        self.cfg.read('.config.ini')

        self.mainlabel = self.findChild(QtWidgets.QLabel, 'mainlabel')
        import datetime
        now = datetime.datetime.now()

        self.mainlabel.setText("Magtess inversion with tesseroids v" + str(gmi_misc.version()) + "\nEldar Baykiev, " + str(now.year))

        self.gmi_path = self.findChild(QtWidgets.QLineEdit, 'gmi_path')
        self.gmi_path.setText(self.cfg.get('PATH', 'GMI_PATH'))
        self.gmi_path.textChanged.connect(self.set_path)

        self.gmi_tessutil_filename = self.findChild(QtWidgets.QLineEdit, 'gmi_tessutil_filename')
        self.gmi_tessutil_filename.setText(self.cfg.get('PATH', 'GMI_MAGNETIZER'))
        self.gmi_tessutil_filename.textChanged.connect(self.set_tessutil_filename)

        self.gmi_tessbz_filename = self.findChild(QtWidgets.QLineEdit, 'gmi_tessbz_filename')
        self.gmi_tessbz_filename.setText(self.cfg.get('PATH', 'GMI_TESSBZ'))
        self.gmi_tessbz_filename.textChanged.connect(self.set_tessbz_filename)

        self.path_browse = self.findChild(QtWidgets.QPushButton, 'path_browse')
        self.path_browse.clicked.connect(self.get_path)

        self.help1 = self.findChild(QtWidgets.QPushButton, 'help1')
        self.help1.clicked.connect(self.help_path)

        self.tessutil_browse = self.findChild(QtWidgets.QPushButton, 'tessutil_browse')
        self.tessutil_browse.clicked.connect(self.get_tessutil)

        self.tessbz_browse = self.findChild(QtWidgets.QPushButton, 'tessbz_browse')
        self.tessbz_browse.clicked.connect(self.get_tessbz)

        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')

        self.buttonBox.accepted.connect(self.start_main)
        self.buttonBox.rejected.connect(self.reject)

    def set_path(self):
        self.cfg['PATH']['GMI_PATH'] = self.gmi_path.text()

    def set_tessutil_filename(self):
        self.cfg['PATH']['GMI_MAGNETIZER'] = self.gmi_tessutil_filename.text()

    def set_tessbz_filename(self):
        self.cfg['PATH']['GMI_TESSBZ'] = self.gmi_tessbz_filename.text()

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
        self.cfg['PATH']['GMI_PATH'] = str(pname)
        with open('.config.ini', 'w') as configfile:
            self.cfg.write(configfile)


    def get_tessutil(self):
        fname, typ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Executable (*)")
        self.gmi_tessutil_filename.setText(fname)
        self.cfg['PATH']['GMI_MAGNETIZER'] = fname
        with open('.config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def get_tessbz(self):
        fname, typ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Executable (*)")
        self.gmi_tessbz_filename.setText(fname)
        self.cfg['PATH']['GMI_TESSBZ'] = fname
        with open('.config.ini', 'w') as configfile:
            self.cfg.write(configfile)

    def start_main(self):


        if not os.path.exists(self.cfg.get('PATH', 'GMI_PATH')):
            gmi_misc.warning('Select new working folder path')
            return

        if not os.path.exists(self.cfg.get('PATH', 'GMI_MAGNETIZER')):
            gmi_misc.warning('Select new path to tessutil_magnetize_model')
            return

        if not os.path.exists(self.cfg.get('PATH', 'GMI_TESSBZ')):
            gmi_misc.warning('Select new path to tessbz')
            return

        HARDMODE = True

        if not HARDMODE:
            try:
                shutil.copyfile(self.cfg.get('PATH', 'GMI_MAGNETIZER'), self.cfg.get('PATH', 'GMI_PATH') + '/tessutil_magnetize_model')
                os.chmod(self.cfg.get('PATH', 'GMI_PATH') + '/tessutil_magnetize_model', st.st_mode | stat.S_IEXEC)
            except:
                gmi_misc.warning('Could not copy executable ' + self.cfg.get('PATH', 'GMI_MAGNETIZER') + ' to the working folder ' + self.cfg.get('PATH', 'GMI_PATH'))

            try:
                shutil.copyfile(self.cfg.get('PATH', 'GMI_TESSBZ'), self.cfg.get('PATH', 'GMI_PATH') + '/tessbz')
                os.chmod(self.cfg.get('PATH', 'GMI_PATH') + '/tessbz', st.st_mode | stat.S_IEXEC)
            except:
                gmi_misc.warning('Could not copy executable ' + self.cfg.get('PATH', 'GMI_TESSBZ') + ' to the working folder ' + self.cfg.get('PATH', 'GMI_PATH'))
        else:
            os.system('cp ' + self.cfg.get('PATH', 'GMI_MAGNETIZER').replace(' ', '\ ') + ' ' + self.cfg.get('PATH', 'GMI_PATH').replace(' ', '\ ') + '/tessutil_magnetize_model')
            os.system('cp ' + self.cfg.get('PATH', 'GMI_TESSBZ').replace(' ', '\ ') + ' ' + self.cfg.get('PATH', 'GMI_PATH').replace(' ', '\ ') + '/tessbz')

            CHMOD = ''

            import sys

            if sys.platform == 'linux':
                CHMOD = 'chmod +x'

            elif sys.platform == 'darwin':
                CHMOD = 'chmod 755'
            else:
                gmi_misc.error('Unsupported operating system')

            os.system(CHMOD + ' ' + (self.cfg.get('PATH', 'GMI_PATH')).replace(' ', '\ ') + '/tessutil_magnetize_model')
            os.system(CHMOD + ' ' + (self.cfg.get('PATH', 'GMI_PATH')).replace(' ', '\ ') + '/tessbz')




        with open('.config.ini', 'w') as configfile:
            self.cfg.write(configfile)
        self.accept()
