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
        os.chdir(pth)
    except:
        gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ pth + ', ABORTING...')
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

        #plots
        self.plot_scene = QtWidgets.QGraphicsScene()
        self.plot_view = self.findChild(QtWidgets.QGraphicsView, 'plot_view')

        self.button_plot = self.findChild(QtWidgets.QPushButton, 'button_plot')
        self.button_plot.clicked.connect(self.plot)

        self.combobox_plot = self.findChild(QtWidgets.QComboBox, 'combobox_plot')
        self.combobox_plot.currentIndexChanged.connect(self.activate_plot_button)


    def set_path(self, wpath):
        self.GMI_PATH = wpath
        print(self.GMI_PATH)

    def read_config(self):
        with open(self.GMI_PATH + '/input.txt', 'r') as config_file:
            buf = config_file.read()
            self.config_editor.setText(buf)

        import configparser
        import gmi_config

        old_cwd = switch_path(self.GMI_PATH)
        config = gmi_config.read_config()

        print(config)
        self.combobox_plot.clear()
        self.combobox_plot.addItem('TOP_SURFACE')
        self.combobox_plot.addItem('BOT_SURFACE')
        self.combobox_plot.addItem('OBSERVED_DATA')
        self.combobox_plot.addItem('SUBTRACT_DATA')
        self.combobox_plot.addItem('INIT_SOLUTION')
        #self.combobox_plot.addItem(config[])

        switch_path_back(old_cwd)

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

    def activate_plot_button(self):
        import gmi_config
        import gmi_gmt
        import os
        old_cwd = switch_path(self.GMI_PATH)

        config = gmi_config.read_config()
        current_opt = str(self.combobox_plot.currentText())

        for sect in config.sections():
            if(config.has_option(sect, current_opt)):
                if(os.path.exists(config.get(sect, current_opt))):
                    gmi_misc.info(str(sect) + '.'+ str(current_opt) +' (' + config.get(sect, current_opt) + ') is selected for plotting')
                    self.button_plot.setEnabled(True)
                    self.button_plot.show()
                    break

                else:
                    gmi_misc.warning(str(sect) + '.'+ str(current_opt) +' (' + config.get(sect, current_opt) + ') IS EMPTY/DOES NOT EXIST!')
                    self.button_plot.setDisabled(True)
                    self.button_plot.show()
                    break

        switch_path_back(old_cwd)


    def plot(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        config = gmi_config.read_config()

        fname = ''
        pname = ''
        uname = ''
        units = ''
        colorsch = ''
        min = 0
        max = 0
        surf = False
        current_plot = str(self.combobox_plot.currentText())
        if current_plot == 'TOP_SURFACE':
            fname = config.get('Global Tesseroid Model', 'TOP_SURFACE');
            pname = 'Top Surface'
            colorsch = 'haxby'
            uname = 'Depth'
            units = 'kM'
            min = -10
            max = 15
            surf = True

            grid = gmi_misc.read_surf_grid(fname)
            grid = grid / 1000.0

        elif current_plot == 'BOT_SURFACE':
            fname = config.get('Global Tesseroid Model', 'BOT_SURFACE');

            pname = 'Top Surface'
            colorsch = 'haxby'
            uname = 'Depth'
            units = 'kM'
            min = -70
            max = -5
            surf = True

            grid = gmi_misc.read_surf_grid(fname)
            grid = grid / 1000.0

        elif current_plot == 'OBSERVED_DATA':
            fname = config.get('Inversion', 'OBSERVED_DATA');
            pname = 'Observed Field'
            colorsch = 'polar'
            uname = 'Magnetic field'
            units = 'nT'
            min = -12
            max = 12
            surf = False

            grid = gmi_misc.read_data_grid(fname)

        elif current_plot == 'SUBTRACT_DATA':
            fname = config.get('Inversion', 'SUBTRACT_DATA');

            pname = 'Field to be Removed from Observed'
            colorsch = 'polar'
            uname = 'Magnetic field'
            units = 'nT'
            min = -12
            max = 12
            surf = False

            grid = gmi_misc.read_data_grid(fname)
        elif current_plot == 'INIT_SOLUTION':
            x0_name = config.get('Inversion', 'INIT_SOLUTION');
            pname = 'Initial solution'
            colorsch = 'haxby'
            uname = 'Susceptibility'
            units = 'SI'
            min = 0
            max = 0.1

            x0 = np.loadtxt(x0_name)

        else:
            pass

        gmi_gmt.plot_global_grid(grid, surf, pname, min, max, colorsch, uname, units)

        print (fname)
        print("PLOT!!!")

        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.plot_scene.addPixmap(plot_pixmap.scaledToHeight(self.plot_view.geometry().height()*0.95))
        #self.plot_scene.setSceneRect(self.plot_view.geometry().x(), self.plot_view.geometry().y(), self.plot_view.geometry().width(), self.plot_view.geometry().height())

        self.plot_view.setScene(self.plot_scene)
        self.plot_view.show()

        switch_path_back(old_cwd)

    def plot_observed(self):
        old_cwd = switch_path(self.GMI_PATH)

        import gmi_gmt

        import matplotlib.pyplot as plt

        import gmi_config
        gmi_config.read_config()


        switch_path_back(old_cwd)

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
