'''
Created on Jul 23, 2018

@author: kaess
'''

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

from PyQt5.QtWidgets import QWidget

from Ui_FITSViewerV2 import Ui_Form
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from util import fix
from util import fixFlipped
from util import flipRHS


class FITSViewer(QWidget):
    '''
    classdocs
    '''    

    def __init__(self, dataCube):
        super(FITSViewer, self).__init__()
        '''
        Constructor
        '''
        # Set up the user interface from Designer.
        if np.size(np.shape(dataCube)) == 2:
            self.rawDataCube = np.array([dataCube])
        else:
            self.rawDataCube = dataCube
        self.dataCube = self.rawDataCube
        self.N = np.size(dataCube, 0)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.toolbar = NavigationToolbar(self.ui.canvas,self)
        self.fig = self.layout().itemAt(0).widget().figure.subplots()
        self.Diff = False  # False for frame, True for diff
        # Make some local modifications.
        self._imdraw(0)
        # Connect up the buttons.
        self.ui.spinBox.setRange(0, self.N - 1)
        self.ui.spinBox.valueChanged.connect(self.valueChanged)
        self.ui.radioButton.clicked.connect(self.frameClicked)
        self.ui.radioButton_2.clicked.connect(self.diffClicked)
        self.ui.radioButton_3.clicked.connect(self.noneClicked)
        self.ui.radioButton_5.clicked.connect(self.flipRHSClicked)
        self.ui.radioButton_4.clicked.connect(self.autofixClicked)
        self.ui.radioButton_6.clicked.connect(self.fixFlippedClicked)
        #self.ui.pushButton.clicked.connect(self.buttonclicked)
        
    def _imdraw(self, i):
        #self.ui.canvas.figure.clf(keep_observers=True)
        #self.fig = self.ui.canvas.figure.subplots()
        self.fig.cla()
        if self.Diff:
            self.fig.imshow(np.subtract(self.dataCube[i, :, :], self.dataCube[i - 1, :, :]))
        else:
            self.fig.imshow(self.dataCube[i, :, :])
        self.ui.canvas.draw_idle()
    
    def valueChanged(self, i):
        self._imdraw(i)
    
    def frameClicked(self):
        if self.Diff:
            self.Diff = False
            self.ui.spinBox.setRange(0, self.N - 1)  # may require toggling event generation for spinBox
            self._imdraw(self.ui.spinBox.value())
    
    def diffClicked(self):
        if not self.Diff:
            self.Diff = True
            self.ui.spinBox.setRange(1, self.N - 1)
            self._imdraw(self.ui.spinBox.value())
            
    def noneClicked(self):
        self.dataCube = self.rawDataCube
        self._imdraw(self.ui.spinBox.value())
        
    def flipRHSClicked(self): #generalize later
        self.dataCube = flipRHS(self.rawDataCube)
        self._imdraw(self.ui.spinBox.value())
        
    def fixFlippedClicked(self):
        self.dataCube = fixFlipped(self.rawDataCube)
        self._imdraw(self.ui.spinBox.value())
        
    def autofixClicked(self):
        self.datCube = fix(self.rawDataCube)
        self._imdraw(self.ui.spinBox.value())
        #fix left off by one
        #self.dataCube = np.concantenate((np.concatenate(())))
        
    #def buttonclicked(self):
    #    print("Sigma: {}".format(self.ui.sigma.value()))
    #    print("Iterations: {}".format(self.ui.iterations.value()))
