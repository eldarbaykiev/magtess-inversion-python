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
import numpy as np

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gmi_mainwindow.ui", self)

        #opened path

        self.working_directory_opened = False
        self.GMI_PATH = ''

        self.current_folder = self.findChild(QtWidgets.QLabel, 'current_folder')
        self.current_folder.setText(self.GMI_PATH)

        self.button_changefolder = self.findChild(QtWidgets.QPushButton, 'button_changefolder')
        self.button_changefolder.clicked.connect(self.open_working_directory)

        #config editor
        self.config_editor = self.findChild(QtWidgets.QTextEdit, 'config_editor')
        self.config_editor.textChanged.connect(self.activate_save)

        self.button_save = self.findChild(QtWidgets.QPushButton, 'button_save')
        self.button_save.clicked.connect(self.save_config)

        #self.button_check = self.findChild(QtWidgets.QPushButton, 'button_checksum')
        #self.button_check.clicked.connect(self.check_hashtest)

        self.button_close = self.findChild(QtWidgets.QPushButton, 'button_close')
        self.button_close.clicked.connect(self.close)

        #self.button_observed = self.findChild(QtWidgets.QPushButton, 'button_observed')
        #self.button_observed.clicked.connect(self.plot_observed)

        #plots
        self.plot_scene = QtWidgets.QGraphicsScene()
        self.plot_view = self.findChild(QtWidgets.QGraphicsView, 'plot_view')

        self.button_plot = self.findChild(QtWidgets.QPushButton, 'button_plot')
        self.button_plot.clicked.connect(self.plot)

        self.combobox_plot = self.findChild(QtWidgets.QComboBox, 'combobox_plot')
        self.combobox_plot.currentIndexChanged.connect(self.activate_plot_button)

        #stages
        self.checksums = False
        self.checkbox_checksums = self.findChild(QtWidgets.QCheckBox, 'checkbox_checksums')
        if self.checksums:
            self.checkbox_checksums.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox_checksums.setCheckState(QtCore.Qt.Unchecked)
        self.checkbox_checksums.stateChanged.connect(self.set_checksums)

        self.stages_updated = False
        self.tabs = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tabs.currentChanged.connect(self.update_stages)

        self.button_stage1 = self.findChild(QtWidgets.QPushButton, 'button_stage1')
        self.button_stage1.clicked.connect(self.run_stage1)
        self.indicator_stage1 = self.findChild(QtWidgets.QLabel, 'indicator_stage1')

        self.button_stage2 = self.findChild(QtWidgets.QPushButton, 'button_stage2')
        self.button_stage2.clicked.connect(self.run_stage2)
        self.indicator_stage2 = self.findChild(QtWidgets.QLabel, 'indicator_stage2')

        self.button_stage3 = self.findChild(QtWidgets.QPushButton, 'button_stage3')
        self.button_stage3.clicked.connect(self.run_stage3)
        self.indicator_stage3 = self.findChild(QtWidgets.QLabel, 'indicator_stage3')

        self.button_allstages = self.findChild(QtWidgets.QPushButton, 'button_allstages')
        self.button_allstages.clicked.connect(self.run_allstages)

        #self.console = self.findChild(QtWidgets.QTextBrowser, 'console')

        #inversion
        self.button_invert = self.findChild(QtWidgets.QPushButton, 'button_invert')
        self.button_invert.clicked.connect(self.run_stage4)

        #self.button_plotresult = self.findChild(QtWidgets.QPushButton, 'button_plotresult')
        #self.button_plotresult.clicked.connect(self.plot_result)

        self.result_list = self.findChild(QtWidgets.QListWidget, 'result_list')
        self.result_list.currentItemChanged.connect(self.activate_plot_result_button)

        self.result_scene = QtWidgets.QGraphicsScene()
        self.result_view = self.findChild(QtWidgets.QGraphicsView, 'result_view')

        if not self.working_directory_opened:
            self.open_working_directory()

    def activate_plot_result_button(self):
        import gmi_config
        import gmi_gmt
        import os
        old_cwd = switch_path(self.GMI_PATH)

        config = gmi_config.read_config()
        current_opt = str(self.result_list.currentItem().text())

        self.result_list.repaint()

        print (current_opt)

        if(os.path.exists(current_opt)):
            gmi_misc.info(str(current_opt) + ' is selected for plotting')
            #self.button_plotresult.setEnabled(True)
            self.result_view.setEnabled(True)
            #self.button_plotresult.repaint()
        else:
            #self.button_plotresult.setDisabled(True)
            self.result_view.setDisabled(True)
            #self.button_plotresult.repaint()


        switch_path_back(old_cwd)

        self.plot_result()

    def plot_result(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        self.result_scene.clear() #new thing

        config = gmi_config.read_config()

        output_folder = gmi_misc.init_result_folder()

        fname = ''
        pname = ''
        uname = ''
        units = ''
        colorsch = ''
        min = 0
        max = 0
        surf = False
        current_plot = output_folder + '/' + str(self.result_list.currentItem().text())

        pname = 'Itest'
        colorsch = 'haxby'
        uname = 'test'
        units = 'test'
        min = 0
        max = 0.1

        grid = gmi_misc.read_sus_grid(current_plot)

        gmi_gmt.plot_global_grid(grid, surf, pname, min, max, colorsch, uname, units)

        result_pixmap =  QtGui.QPixmap('temp.png')
        self.result_scene.addPixmap(result_pixmap.scaledToHeight(self.result_view.geometry().height()*0.95))

        self.result_view.setScene(self.result_scene)
        self.result_view.show()

        import shutil
        shutil.copyfile('temp.png', './' + output_folder + '/' + self.result_list.currentItem().text()[:-3]+ 'png')

        switch_path_back(old_cwd)


    def set_checksums(self):

        if self.checkbox_checksums.isChecked():
            self.checksums = True

            self.stages_updated = False
            self.update_stages()
            print('checksums True')
        else:
            self.checksums = False

            self.stages_updated = False
            self.update_stages()
            print('checksums False')


    def update_stages(self):

        if self.tabs.currentWidget().objectName() == 'tab_stages' and self.stages_updated == False:

            pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
            self.indicator_stage1.setPixmap(pixmap)
            self.indicator_stage1.repaint()
            self.indicator_stage2.setPixmap(pixmap)
            self.indicator_stage2.repaint()
            self.indicator_stage3.setPixmap(pixmap)
            self.indicator_stage3.repaint()

            import gmi_hash_test
            stages = [0, 0, 0]
            stages, dict = gmi_hash_test.main(self.GMI_PATH, tc=self.checksums)

            pixmap_checked =  QtGui.QPixmap('icons/icons8-checkmark-48.png')
            pixmap_doublechecked =  QtGui.QPixmap('icons/icons8-double-tick-48.png')
            pixmap_unchecked =  QtGui.QPixmap('icons/icons8-delete-48.png')

            self.button_stage1.setEnabled(True)
            self.button_stage2.setEnabled(False)
            self.button_stage3.setEnabled(False)

            if stages[0] > 0:
                if self.checksums:
                    self.indicator_stage1.setPixmap(pixmap_doublechecked)
                else:
                    self.indicator_stage1.setPixmap(pixmap_checked)
                self.button_stage2.setEnabled(True)
                #self.button_stage3.setEnabled(False)
                #self.label_stage1.setText('correct checksum')
            elif stages[0] == 0:
                self.indicator_stage1.setPixmap(pixmap_unchecked)
                self.button_stage2.setEnabled(False)
                #self.label_stage1.setText('no checksum')
            else:
                self.indicator_stage1.setPixmap(pixmap_unchecked)
                self.button_stage2.setEnabled(False)
                #self.label_stage1.setText('checksum in dictionary\ndoes not match')
            self.indicator_stage1.repaint()

            if stages[1] > 0:
                if self.checksums:
                    self.indicator_stage2.setPixmap(pixmap_doublechecked)
                else:
                    self.indicator_stage2.setPixmap(pixmap_checked)
                self.button_stage3.setEnabled(True)
                #self.label_stage2.setText('correct checksum')
            elif stages[0] == 0:
                self.indicator_stage2.setPixmap(pixmap_unchecked)
                self.button_stage3.setEnabled(False)
                #self.label_stage2.setText('no checksum')
            else:
                self.indicator_stage2.setPixmap(pixmap_unchecked)
                self.button_stage3.setEnabled(False)
                #self.label_stage2.setText('checksum in dictionary\ndoes not match')
            self.indicator_stage2.repaint()

            if stages[2] > 0:
                if self.checksums:
                    self.indicator_stage3.setPixmap(pixmap_doublechecked)
                else:
                    self.indicator_stage3.setPixmap(pixmap_checked)
                #self.label_stage3.setText('correct checksum')
            elif stages[0] == 0:
                self.indicator_stage3.setPixmap(pixmap_unchecked)
                #self.label_stage3.setText('no checksum')
            else:
                self.indicator_stage3.setPixmap(pixmap_unchecked)
                #self.label_stage3.setText('checksum in dictionary\ndoes not match')
            self.indicator_stage3.repaint()


            self.stages_updated = True



    def run_stage1(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.indicator_stage1.setPixmap(pixmap)
        self.indicator_stage1.repaint()

        import gmi_create_tesseroid_model
        old_cwd = switch_path(self.GMI_PATH)

        '''
        self.oldstdout = sys.stdout

        from io import StringIO
        sys.stdout = StringIO()
        # Do processing stages
        # And later
        '''

        print('stage1')
        gmi_create_tesseroid_model.main(self.GMI_PATH)
        '''
        self.console.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout
        '''
        switch_path_back(old_cwd)

        self.stages_updated = False
        self.update_stages()



    def run_stage2(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.indicator_stage2.setPixmap(pixmap)
        self.indicator_stage2.repaint()

        import gmi_calculate_effect_of_each_tesseroid
        old_cwd = switch_path(self.GMI_PATH)

        '''
        self.oldstdout = sys.stdout
        from io import StringIO
        sys.stdout = StringIO()
        # Do processing stages
        # And later
        '''

        print('stage2')
        gmi_calculate_effect_of_each_tesseroid.main(self.GMI_PATH)
        '''
        self.console.setText( sys.stdout.getvalue() )
        sys.stdout = self.oldstdout
        '''
        switch_path_back(old_cwd)

        self.stages_updated = False
        self.update_stages()


    def run_stage3(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.indicator_stage2.setPixmap(pixmap)
        self.indicator_stage2.repaint()

        import gmi_create_design_matrix
        old_cwd = switch_path(self.GMI_PATH)

        print('stage3')
        gmi_create_design_matrix.main(self.GMI_PATH)

        switch_path_back(old_cwd)

        self.stages_updated = False
        self.update_stages()

    def run_allstages(self):
        self.run_stage1()
        self.run_stage2()
        self.run_stage3()


    #inversion
    def run_stage4(self):
        self.result_scene.clear()

        self.result_view.setDisabled(True)

        self.result_list.clear()
        self.result_list.setDisabled(True)

        import gmi_invert
        old_cwd = switch_path(self.GMI_PATH)

        print('stage4')
        gmi_invert.main(self.GMI_PATH)

        import glob
        output_folder = gmi_misc.init_result_folder()

        os.chdir(output_folder)
        file_list = glob.glob("*.xyz")
        os.chdir('..')

        self.result_list.clear()

        self.result_list.setEnabled(True)
        for filename in file_list:
            self.result_list.addItem(filename)

        switch_path_back(old_cwd)


    def set_path(self, wpath):
        self.GMI_PATH = wpath
        self.current_folder.setText(self.GMI_PATH)
        gmi_misc.info(self.GMI_PATH + ' is set as a working directory')

    def open_working_directory(self):

        if self.working_directory_opened:
            self.save_config()

        pathselection = gmi_pathdialog.PathDialog()
        if not pathselection.exec_(): # 'reject': user pressed 'Cancel', so quit
            if self.working_directory_opened:
                return
            else:
                exit()

        self.set_path(pathselection.cfg.get('PATH', 'GMI_PATH'))

        self.read_working_directory()
        self.plot_scene.clear()

        self.stages_updated = False
        self.update_stages()


        self.working_directory_opened = True


    def read_working_directory(self):
        with open(self.GMI_PATH + '/input.txt', 'r') as config_file:
            buf = config_file.read()
            self.config_editor.setText(buf)

        import configparser
        import gmi_config

        old_cwd = switch_path(self.GMI_PATH)
        config = gmi_config.read_config()

        self.combobox_plot.clear()
        self.combobox_plot.addItem('TOP_SURFACE')
        self.combobox_plot.addItem('BOT_SURFACE')
        self.combobox_plot.addItem('OBSERVED_DATA')
        self.combobox_plot.addItem('SUBTRACT_DATA')
        self.combobox_plot.addItem('INIT_SOLUTION')
        #self.combobox_plot.addItem(config[])

        switch_path_back(old_cwd)

        self.working_directory_opened = True

    def activate_save(self):
        self.button_save.setText('Save')
        self.button_save.setEnabled(True)
        self.button_save.repaint()

    def save_config(self):
        buf = self.config_editor.toPlainText()
        with open(self.GMI_PATH + '/input.txt', 'w') as config_file:
            config_file.write(buf)

        self.button_save.setText('Save')
        self.button_save.setEnabled(False)
        self.button_save.repaint()
        gmi_misc.info('input.txt saved')


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
                    self.plot_view.setEnabled(True)
                    self.button_plot.repaint()
                    break

                else:
                    gmi_misc.warning(str(sect) + '.'+ str(current_opt) +' (' + config.get(sect, current_opt) + ') IS EMPTY/DOES NOT EXIST!')
                    self.button_plot.setDisabled(True)
                    self.plot_view.setDisabled(True)
                    self.button_plot.repaint()
                    break

        switch_path_back(old_cwd)

    def plot(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        self.plot_scene.clear() #new thing

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

            grid = gmi_misc.read_surf_grid(fname)

        elif current_plot == 'SUBTRACT_DATA':
            fname = config.get('Inversion', 'SUBTRACT_DATA');

            pname = 'Field to be Removed from Observed'
            colorsch = 'polar'
            uname = 'Magnetic field'
            units = 'nT'
            min = -12
            max = 12
            surf = False

            grid = gmi_misc.read_surf_grid(fname)
        elif current_plot == 'INIT_SOLUTION':
            x0_name = config.get('Inversion', 'INIT_SOLUTION');
            pname = 'Initial solution'
            colorsch = 'haxby'
            uname = 'Susceptibility'
            units = 'SI'
            min = 0
            max = 0.1

            grid = gmi_misc.read_sus_grid(x0_name)
            #if float(config.get('Inversion', 'MULTIPLICATOR')) != 1.0:
            #    max = max * float(config.get('Inversion', 'MULTIPLICATOR'))
             #   #units = 'SI'.format(float(config.get('Inversion', 'MULTIPLICATOR')))


        else:
            pass

        gmi_gmt.plot_global_grid(grid, surf, pname, min, max, colorsch, uname, units)

        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.plot_scene.addPixmap(plot_pixmap.scaledToHeight(self.plot_view.geometry().height()*0.95))
        #self.plot_scene.setSceneRect(self.plot_view.geometry().x(), self.plot_view.geometry().y(), self.plot_view.geometry().width(), self.plot_view.geometry().height())

        self.plot_view.setScene(self.plot_scene)
        self.plot_view.show()

        output_folder = gmi_misc.init_result_folder()

        import shutil
        shutil.copyfile('temp.png', './' + output_folder + '/' + current_plot+ '.png')

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

    pathselection = gmi_pathdialog.PathDialog()
    if not pathselection.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)

    window = MainWindow()

    window.read_working_directory()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
