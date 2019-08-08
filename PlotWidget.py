'''
Created on Jul 25, 2019

@author: kaess
'''

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT
from PyQt5 import QtWidgets
from matplotlib.figure import Figure

class PlotWidget(QtWidgets.QWidget):
    '''
    classdocs
    '''
    __figure__ = None
    __canvas__ = None

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.__figure__ = Figure()
        self.__canvas__ = FigureCanvas(self.__figure__)
        self.__figure__.set_canvas(self.__canvas__)
        self.layout().addWidget(self.__canvas__)
        self.layout().setMenuBar(NavigationToolbar2QT(self.__canvas__,self))

    def repaint(self):
        if self.__canvas__ is not None:
            self.__canvas__.draw_idle()
        return QtWidgets.QWidget.repaint(self)


    def get_figure(self):
        return self.__figure__


    def get_canvas(self):
        return self.__canvas__
