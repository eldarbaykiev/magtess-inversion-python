# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import gmi_pathdialog, gmi_helpwindow

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

        if sys.platform == 'darwin':
            uic.loadUi("gmi_mainwindow.ui", self)
        elif sys.platform == 'linux':
            uic.loadUi("gmi_mainwindow_linux.ui", self)
        else:
            uic.loadUi("gmi_mainwindow.ui", self)


        #opened path

        self.working_directory_opened = False
        self.GMI_PATH = ''


        #main window

        self.label_CurrentFolder = self.findChild(QtWidgets.QLabel, 'label_CurrentFolder')
        self.label_CurrentFolder.setText(self.GMI_PATH)

        self.pushButton_ChangeFolder = self.findChild(QtWidgets.QPushButton, 'pushButton_ChangeFolder')
        self.pushButton_ChangeFolder.clicked.connect(self.OpenWorkingDirectory)

        self.pushButton_Exit = self.findChild(QtWidgets.QPushButton, 'pushButton_Exit')
        self.pushButton_Exit.clicked.connect(self.close)


        #config editor tab
        self.textEdit_ConfigEditor = self.findChild(QtWidgets.QTextEdit, 'textEdit_ConfigEditor')
        self.textEdit_ConfigEditor.textChanged.connect(self.EnableConfigSave)

        self.pushButton_SaveConfig = self.findChild(QtWidgets.QPushButton, 'pushButton_SaveConfig')
        self.pushButton_SaveConfig.clicked.connect(self.SaveConfig)


        #plots
        self.zoomfactor = 0.95
        self.graphicsScene_PlotScene = QtWidgets.QGraphicsScene()
        self.graphicsView_PlotView = self.findChild(QtWidgets.QGraphicsView, 'graphicsView_PlotView')

        self.pushButton_Plot = self.findChild(QtWidgets.QPushButton, 'pushButton_Plot')
        self.pushButton_Plot.clicked.connect(self.plot)

        self.pushButton_Spectrum = self.findChild(QtWidgets.QPushButton, 'pushButton_Spectrum')
        self.pushButton_Spectrum.clicked.connect(self.spec)

        self.pushButton_ZoomIn = self.findChild(QtWidgets.QPushButton, 'pushButton_ZoomIn')
        self.pushButton_ZoomIn.clicked.connect(self.plot_zoomin)

        self.pushButton_ZoomOut = self.findChild(QtWidgets.QPushButton, 'pushButton_ZoomOut')
        self.pushButton_ZoomOut.clicked.connect(self.plot_zoomout)

        self.comboBox_GridList = self.findChild(QtWidgets.QComboBox, 'comboBox_GridList')
        self.comboBox_GridList.currentIndexChanged.connect(self.EnablePlotting)

        #stages
        self.checksums = False
        self.checkBox_InspectChecksums = self.findChild(QtWidgets.QCheckBox, 'checkBox_InspectChecksums')
        if self.checksums:
            self.checkBox_InspectChecksums.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_InspectChecksums.setCheckState(QtCore.Qt.Unchecked)
        self.checkBox_InspectChecksums.stateChanged.connect(self.InspectChecksums)

        self.stages_updated = False
        self.tabs = self.findChild(QtWidgets.QTabWidget, 'tabWidget_MainTabs')
        self.tabs.currentChanged.connect(self.UpdateStages)

        self.pushButton_CreateTesseroidModel = self.findChild(QtWidgets.QPushButton, 'pushButton_CreateTesseroidModel')
        self.pushButton_CreateTesseroidModel.clicked.connect(self.CreateTesseroidModel)
        self.label_IndicatorCreateTesseroidModel = self.findChild(QtWidgets.QLabel, 'label_IndicatorCreateTesseroidModel')

        self.pushButton_CalculateTesseroidsFields = self.findChild(QtWidgets.QPushButton, 'pushButton_CalculateTesseroidsFields')
        self.pushButton_CalculateTesseroidsFields.clicked.connect(self.CalculateTesseroidsFields)
        self.label_IndicatorCalculateTesseroidsFields = self.findChild(QtWidgets.QLabel, 'label_IndicatorCalculateTesseroidsFields')

        self.pushButton_CreateDesignMatrix = self.findChild(QtWidgets.QPushButton, 'pushButton_CreateDesignMatrix')
        self.pushButton_CreateDesignMatrix.clicked.connect(self.CreateDesignMatrix)
        self.label_IndicatorCreateDesignMatrix = self.findChild(QtWidgets.QLabel, 'label_IndicatorCreateDesignMatrix')

        self.pushButton_ExecuteAll = self.findChild(QtWidgets.QPushButton, 'pushButton_ExecuteAll')
        self.pushButton_ExecuteAll.clicked.connect(self.ExecuteAll)

        #inversion
        self.pushButton_Invert = self.findChild(QtWidgets.QPushButton, 'pushButton_Invert')
        self.pushButton_Invert.clicked.connect(self.Invert)

        self.listWidget_ResultsList = self.findChild(QtWidgets.QListWidget, 'listWidget_ResultsList')
        self.listWidget_ResultsList.currentItemChanged.connect(self.EnableResultPlotting)

        self.graphicsScene_ResultPlotScene = QtWidgets.QGraphicsScene()
        self.graphicsView_ResultPlotView = self.findChild(QtWidgets.QGraphicsView, 'graphicsView_ResultPlotView')

        if not self.working_directory_opened:
            self.OpenWorkingDirectory()

    def EnableResultPlotting(self):
        import gmi_config
        import gmi_gmt
        import os
        old_cwd = switch_path(self.GMI_PATH)

        config = gmi_config.read_config()
        try:
            current_opt = str(self.listWidget_ResultsList.currentItem().text())
        except:
            current_opt = '_none_'
            gmi_misc.debug('bug to fix with restarting inversion win new paramters')

        self.listWidget_ResultsList.repaint()

        print (current_opt)

        if(os.path.exists(current_opt)):
            gmi_misc.info(str(current_opt) + ' is selected for plotting')
            #self.pushButton_Plotresult.setEnabled(True)
            self.graphicsView_ResultPlotView.setEnabled(True)
            #self.pushButton_Plotresult.repaint()
        else:
            #self.pushButton_Plotresult.setDisabled(True)
            self.graphicsView_ResultPlotView.setDisabled(True)
            #self.pushButton_Plotresult.repaint()


        switch_path_back(old_cwd)

        self.PlotResult()

    def PlotResult(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        self.graphicsScene_ResultPlotScene.clear() #new thing

        config = gmi_config.read_config()

        output_folder = gmi_misc.init_result_folder()

        fname = str(self.listWidget_ResultsList.currentItem().text())

        indrem = 3

        if '.dat' in fname:
            current_plot = output_folder + '/' + fname

            dat = np.loadtxt(current_plot)

            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.plot(dat[:, 0], dat[:, 1])

            ax.set(xlabel='i', ylabel='val',
                   title='.dat file plot')
            ax.grid()

            fig.savefig("temp.png")
            #plt.show()

            plt.clf()
            plt.close()

            indrem = 3



        elif '.spec' in fname:
            current_plot = output_folder + '/' + fname

            dat = np.loadtxt(current_plot)

            import matplotlib.pyplot as plt

            plt.plot(dat[1:, 0], np.log10(dat[:, 1])[1:], '-', lw=0.6)

            a_yticks = np.array([1, 0.1, 0.01, 0.001, 0.0001])
            plt.yticks(np.log10(a_yticks), a_yticks.astype(str))

            a_xticks = np.append(np.array([1]),  np.arange(10, np.ndarray.max(dat[:, 0]), 10))
            a_xticks = np.append(a_xticks, np.array([int(config.get('Spherical Harmonics', 'N_MIN_CUTOFF'))]))
            plt.xticks(a_xticks, a_xticks.astype(str))

            plt.title(current_plot + ' power spectrum')
            plt.xlabel('SH degree')
            plt.ylabel('Power [SI^2]')
            plt.grid()


            plt.savefig('temp.png')

            plt.clf()
            plt.close()

            indrem = 4

        elif '.sht_shcoeff' in fname:
            import pyshtools
            import matplotlib.pyplot as plt
            urrent_plot = output_folder + '/' + fname

            sht_shcoeff = pyshtools.SHCoeffs.from_file(fname)
            sht_shcoeff.plot_spectrum2d()

            plt.savefig('temp.png')

            plt.clf()
            plt.close()

            indrem = 11


        else:
            current_plot = output_folder + '/' + fname
            surf = False

            if 'grid' in fname:


                pname = fname
                colorsch = 'polar'
                uname = 'Magnetic Field'
                units = 'nT'
                min = -12
                max = 12

                grid = gmi_misc.read_surf_grid(current_plot)
            else:

                pname = fname
                colorsch = 'haxby'
                uname = 'Susceptibility'
                units = 'SI'
                min = 0
                max = 0.1

                grid = gmi_misc.read_sus_grid(current_plot)

            indrem = 3

            if gmi_config.T_DO_TILES:
                type_p = 2
            else:
                type_p = 1

            gmi_gmt.plot_global_grid(grid, surf, pname, min, max, colorsch, uname, units, type_p)


        result_pixmap =  QtGui.QPixmap('temp.png')
        self.graphicsScene_ResultPlotScene.addPixmap(result_pixmap.scaledToHeight(self.graphicsView_ResultPlotView.geometry().height()*0.95))

        self.graphicsView_ResultPlotView.setScene(self.graphicsScene_ResultPlotScene)
        self.graphicsView_ResultPlotView.show()

        import shutil
        shutil.copyfile('temp.png', './' + output_folder + '/' + self.listWidget_ResultsList.currentItem().text()[:-indrem]+ 'png')

        switch_path_back(old_cwd)


    def InspectChecksums(self):
        if self.checkBox_InspectChecksums.isChecked():
            self.checksums = True

            self.stages_updated = False
            self.UpdateStages()
        else:
            self.checksums = False

            self.stages_updated = False
            self.UpdateStages()

    def UpdateStages(self):
        if self.tabs.currentWidget().objectName() == 'tab_stages' and self.stages_updated == False:

            pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
            self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap)
            self.label_IndicatorCreateTesseroidModel.repaint()
            self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap)
            self.label_IndicatorCalculateTesseroidsFields.repaint()
            self.label_IndicatorCreateDesignMatrix.setPixmap(pixmap)
            self.label_IndicatorCreateDesignMatrix.repaint()

            import gmi_hash_test
            stages = [0, 0, 0]
            stages, dict = gmi_hash_test.main(self.GMI_PATH, tc=self.checksums)

            pixmap_checked =  QtGui.QPixmap('icons/icons8-checkmark-48.png')
            pixmap_doublechecked =  QtGui.QPixmap('icons/icons8-double-tick-48.png')
            pixmap_unchecked =  QtGui.QPixmap('icons/icons8-delete-48.png')

            self.pushButton_CreateTesseroidModel.setEnabled(True)
            self.pushButton_CalculateTesseroidsFields.setEnabled(False)
            self.pushButton_CreateDesignMatrix.setEnabled(False)

            if stages[0] > 0:
                if self.checksums:
                    self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap_doublechecked)
                else:
                    self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap_checked)
                self.pushButton_CalculateTesseroidsFields.setEnabled(True)
                #self.pushButton_CreateDesignMatrix.setEnabled(False)
                #self.label_stage1.setText('correct checksum')
            elif stages[0] == 0:
                self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap_unchecked)
                self.pushButton_CalculateTesseroidsFields.setEnabled(False)
                #self.label_stage1.setText('no checksum')
            else:
                self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap_unchecked)
                self.pushButton_CalculateTesseroidsFields.setEnabled(False)
                #self.label_stage1.setText('checksum in dictionary\ndoes not match')
            self.label_IndicatorCreateTesseroidModel.repaint()

            if stages[1] > 0:
                if self.checksums:
                    self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap_doublechecked)
                else:
                    self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap_checked)
                self.pushButton_CreateDesignMatrix.setEnabled(True)
                #self.label_stage2.setText('correct checksum')
            elif stages[0] == 0:
                self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap_unchecked)
                self.pushButton_CreateDesignMatrix.setEnabled(False)
                #self.label_stage2.setText('no checksum')
            else:
                self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap_unchecked)
                self.pushButton_CreateDesignMatrix.setEnabled(False)
                #self.label_stage2.setText('checksum in dictionary\ndoes not match')
            self.label_IndicatorCalculateTesseroidsFields.repaint()

            if stages[2] > 0:
                if self.checksums:
                    self.label_IndicatorCreateDesignMatrix.setPixmap(pixmap_doublechecked)
                else:
                    self.label_IndicatorCreateDesignMatrix.setPixmap(pixmap_checked)
                #self.label_stage3.setText('correct checksum')
            elif stages[0] == 0:
                self.label_IndicatorCreateDesignMatrix.setPixmap(pixmap_unchecked)
                #self.label_stage3.setText('no checksum')
            else:
                self.label_IndicatorCreateDesignMatrix.setPixmap(pixmap_unchecked)
                #self.label_stage3.setText('checksum in dictionary\ndoes not match')
            self.label_IndicatorCreateDesignMatrix.repaint()


            self.stages_updated = True



    def CreateTesseroidModel(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.label_IndicatorCreateTesseroidModel.setPixmap(pixmap)
        self.label_IndicatorCreateTesseroidModel.repaint()

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
        self.UpdateStages()

        QtWidgets.QMessageBox.information(self, "Message", "Tesseroid model created!")



    def CalculateTesseroidsFields(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap)
        self.label_IndicatorCalculateTesseroidsFields.repaint()

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
        self.UpdateStages()

        QtWidgets.QMessageBox.information(self, "Message", "Tesseroids' fields calculated!")


    def CreateDesignMatrix(self):
        pixmap = QtGui.QPixmap('icons/icons8-process-120.png')
        self.label_IndicatorCalculateTesseroidsFields.setPixmap(pixmap)
        self.label_IndicatorCalculateTesseroidsFields.repaint()

        import gmi_create_design_matrix
        old_cwd = switch_path(self.GMI_PATH)

        print('stage3')
        gmi_create_design_matrix.main(self.GMI_PATH)

        switch_path_back(old_cwd)

        self.stages_updated = False
        self.UpdateStages()

        QtWidgets.QMessageBox.information(self, "Message", "Design matrices created")

    def ExecuteAll(self):
        self.CreateTesseroidModel()
        self.CalculateTesseroidsFields()
        self.CreateDesignMatrix()


    #inversion

    def InitResultsList(self):
        self.graphicsScene_ResultPlotScene.clear()
        self.listWidget_ResultsList.clear()


        old_cwd = switch_path(self.GMI_PATH)

        import glob
        output_folder = gmi_misc.init_result_folder()

        os.chdir(output_folder)
        file_list = glob.glob("*.xyz")
        file_list = file_list + glob.glob("*.dat") + glob.glob('*.spec') + glob.glob('*.sht_shcoeff')
        os.chdir('..')

        self.listWidget_ResultsList.clear()

        self.listWidget_ResultsList.setEnabled(True)
        for filename in file_list:
            self.listWidget_ResultsList.addItem(filename)

        switch_path_back(old_cwd)



    def Invert(self):
        self.graphicsScene_ResultPlotScene.clear()
        self.listWidget_ResultsList.clear()
        self.listWidget_ResultsList.setDisabled(True)

        import gmi_invert
        old_cwd = switch_path(self.GMI_PATH)

        print('stage4')
        gmi_invert.main(self.GMI_PATH)

        self.InitResultsList()

        switch_path_back(old_cwd)


    def SetPath(self, wpath):
        self.GMI_PATH = wpath
        self.label_CurrentFolder.setText(self.GMI_PATH)
        gmi_misc.info(self.GMI_PATH + ' is set as a working directory')

    def OpenWorkingDirectory(self):
        if self.working_directory_opened:
            self.SaveConfig()

        pathselection = gmi_pathdialog.PathDialog()
        if not pathselection.exec_(): # 'reject': user pressed 'Cancel', so quit
            if self.working_directory_opened:
                return
            else:
                exit()

        self.SetPath(pathselection.cfg.get('PATH', 'GMI_PATH'))

        self.ReadWorkingDirectory()
        self.graphicsScene_PlotScene.clear()

        self.stages_updated = False
        self.UpdateStages()


        self.working_directory_opened = True


    def ReadWorkingDirectory(self):
        import configparser
        import gmi_config

        old_cwd = switch_path(self.GMI_PATH)
        config = gmi_config.read_config()

        with open(self.GMI_PATH + '/input.txt', 'r') as config_file:
            buf = config_file.read()
            self.textEdit_ConfigEditor.setText(buf)



        self.comboBox_GridList.clear()
        self.comboBox_GridList.addItem('TOP_SURFACE')
        self.comboBox_GridList.addItem('BOT_SURFACE')
        self.comboBox_GridList.addItem('OBSERVED_DATA')
        self.comboBox_GridList.addItem('SUBTRACT_DATA')
        self.comboBox_GridList.addItem('INIT_SOLUTION')
        #self.comboBox_GridList.addItem(config[])

        switch_path_back(old_cwd)

        self.working_directory_opened = True

        self.InitResultsList()

    def EnableConfigSave(self):
        self.pushButton_SaveConfig.setText('Save')
        self.pushButton_SaveConfig.setEnabled(True)
        self.pushButton_SaveConfig.repaint()

    def SaveConfig(self):
        buf = self.textEdit_ConfigEditor.toPlainText()
        with open(self.GMI_PATH + '/input.txt', 'w') as config_file:
            config_file.write(buf)

        self.pushButton_SaveConfig.setText('Save')
        self.pushButton_SaveConfig.setEnabled(False)
        self.pushButton_SaveConfig.repaint()
        gmi_misc.info('input.txt saved')



    def EnablePlotting(self):
        import gmi_config
        import gmi_gmt
        import os
        old_cwd = switch_path(self.GMI_PATH)

        config = gmi_config.read_config()
        current_opt = str(self.comboBox_GridList.currentText())

        for sect in config.sections():
            if(config.has_option(sect, current_opt)):
                if(os.path.exists(config.get(sect, current_opt))):
                    gmi_misc.info(str(sect) + '.'+ str(current_opt) +' (' + config.get(sect, current_opt) + ') is selected for plotting')
                    self.pushButton_Plot.setEnabled(True)
                    self.pushButton_Spectrum.setEnabled(True)
                    self.pushButton_ZoomIn.setEnabled(True)
                    self.pushButton_ZoomOut.setEnabled(True)
                    self.graphicsView_PlotView.setEnabled(True)
                    self.pushButton_Plot.repaint()
                    self.pushButton_Spectrum.repaint()
                    break

                else:
                    gmi_misc.warning(str(sect) + '.'+ str(current_opt) +' (' + config.get(sect, current_opt) + ') IS EMPTY/DOES NOT EXIST!')
                    self.pushButton_Plot.setDisabled(True)
                    self.pushButton_Spectrum.setDisabled(True)
                    self.pushButton_ZoomIn.setDisabled(True)
                    self.pushButton_ZoomOut.setDisabled(True)
                    self.graphicsView_PlotView.setDisabled(True)
                    self.pushButton_Plot.repaint()
                    self.pushButton_Spectrum.repaint()
                    break

        switch_path_back(old_cwd)

    def spec(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        self.graphicsScene_PlotScene.clear() #new thing

        config = gmi_config.read_config()

        plot_cutoff = False

        current_plot = str(self.comboBox_GridList.currentText())
        if current_plot == 'TOP_SURFACE':
            fname = config.get('Global Tesseroid Model', 'TOP_SURFACE');
            grid = gmi_misc.read_surf_grid(fname)
            norm = 'unnorm'
            units = 'kM'
            grid = grid / 1000.0

        elif current_plot == 'BOT_SURFACE':
            fname = config.get('Global Tesseroid Model', 'BOT_SURFACE');
            grid = gmi_misc.read_surf_grid(fname)
            norm = 'unnorm'
            units = 'kM'
            grid = grid / 1000.0

        elif current_plot == 'OBSERVED_DATA':
            fname = config.get('Inversion', 'OBSERVED_DATA');
            norm = 'schmidt'
            units = 'nT'
            plot_cutoff = True
            grid = gmi_misc.read_data_grid(fname)

        elif current_plot == 'SUBTRACT_DATA':
            fname = config.get('Inversion', 'SUBTRACT_DATA');
            norm = 'schmidt'
            units = 'nT'
            plot_cutoff = True
            grid = gmi_misc.read_data_grid(fname)

        elif current_plot == 'INIT_SOLUTION':
            x0_name = config.get('Inversion', 'INIT_SOLUTION');
            norm = 'unnorm'
            units = 'SI'
            grid = gmi_misc.read_sus_grid(x0_name)

        else:
            pass

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import pyshtools

        grid_sht = pyshtools.SHGrid.from_array(grid)
        shc_sht = grid_sht.expand(normalization=norm)
        spectrum = shc_sht.spectrum()

        deg = shc_sht.degrees()
        print(deg)

        #plotting

        plt.plot(deg[1:], np.log10(spectrum)[1:], '-', lw=0.6)

        a_yticks = np.array([1, 0.1, 0.01, 0.001, 0.0001])
        plt.yticks(np.log10(a_yticks), a_yticks.astype(str))

        a_xticks = np.append(np.array([1]), np.arange(10, max(deg), 10))
        if plot_cutoff:
            a_xticks = np.append(a_xticks, np.array([int(config.get('Spherical Harmonics', 'N_MIN_CUTOFF'))]))

        plt.xticks(a_xticks, a_xticks.astype(str))

        plt.title(current_plot + ' power spectrum')
        plt.xlabel('SH degree')
        plt.ylabel('Power [' + units +'^2]')
        plt.grid()


        plt.savefig('temp.png')

        plt.clf()
        plt.close()


        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.graphicsScene_PlotScene.addPixmap(plot_pixmap.scaledToHeight(self.graphicsView_PlotView.geometry().height()*0.95))
        #self.graphicsScene_PlotScene.setSceneRect(self.graphicsView_PlotView.geometry().x(), self.graphicsView_PlotView.geometry().y(), self.graphicsView_PlotView.geometry().width(), self.graphicsView_PlotView.geometry().height())

        self.graphicsView_PlotView.setScene(self.graphicsScene_PlotScene)
        self.graphicsView_PlotView.show()

        output_folder = gmi_misc.init_result_folder()

        import shutil
        shutil.copyfile('temp.png', './' + output_folder + '/' + current_plot+ '_spec.png')

        switch_path_back(old_cwd)



    def plot(self):
        import gmi_config
        import gmi_gmt
        old_cwd = switch_path(self.GMI_PATH)

        self.graphicsScene_PlotScene.clear() #new thing

        config = gmi_config.read_config()

        fname = ''
        pname = ''
        uname = ''
        units = ''
        colorsch = ''
        min = 0
        max = 0
        surf = False
        current_plot = str(self.comboBox_GridList.currentText())
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

        gmi_gmt.plot_global_grid(grid, surf, pname, min, max, colorsch, uname, units, 1)

        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.graphicsScene_PlotScene.addPixmap(plot_pixmap.scaledToHeight(self.graphicsView_PlotView.geometry().height()*self.zoomfactor))
        #self.graphicsScene_PlotScene.setSceneRect(self.graphicsView_PlotView.geometry().x(), self.graphicsView_PlotView.geometry().y(), self.graphicsView_PlotView.geometry().width(), self.graphicsView_PlotView.geometry().height())

        self.graphicsView_PlotView.setScene(self.graphicsScene_PlotScene)
        self.graphicsView_PlotView.show()

        output_folder = gmi_misc.init_result_folder()

        import shutil
        shutil.copyfile('temp.png', './' + output_folder + '/' + current_plot+ '.png')

        switch_path_back(old_cwd)

    def plot_zoomin(self):
        old_cwd = switch_path(self.GMI_PATH)

        self.graphicsScene_PlotScene.clear() #new thing

        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.zoomfactor += 0.1
        self.graphicsScene_PlotScene.addPixmap(plot_pixmap.scaledToHeight(self.graphicsView_PlotView.geometry().height()*self.zoomfactor))

        self.graphicsView_PlotView.setScene(self.graphicsScene_PlotScene)
        self.graphicsView_PlotView.show()

        switch_path_back(old_cwd)

    def plot_zoomout(self):
        old_cwd = switch_path(self.GMI_PATH)

        self.graphicsScene_PlotScene.clear() #new thing

        plot_pixmap =  QtGui.QPixmap('temp.png')
        self.zoomfactor -= 0.1
        self.graphicsScene_PlotScene.addPixmap(plot_pixmap.scaledToHeight(self.graphicsView_PlotView.geometry().height()*self.zoomfactor))

        self.graphicsView_PlotView.setScene(self.graphicsScene_PlotScene)
        self.graphicsView_PlotView.show()

        switch_path_back(old_cwd)

    def close(self):
        exit(0)



def main():
    app = QtWidgets.QApplication(sys.argv)

    pathselection = gmi_pathdialog.PathDialog()
    if not pathselection.exec_(): # 'reject': user pressed 'Cancel', so quit
        sys.exit(-1)

    window = MainWindow()
    window.setFixedSize(QtCore.QSize(window.width(), window.height()) )

    window.ReadWorkingDirectory()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
