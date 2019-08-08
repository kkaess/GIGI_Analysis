'''
Created on Jul 15, 2019

@author: kaess
'''
import numpy as np
from astropy.modeling import models, fitting
from astropy.io import fits

import os.path as path
from copy import deepcopy


class MultiGaussianModel(object):
    '''
    classdocs
    '''
    __vals__ = []
    __wasRun__ = False
    __fitsImage__ = None
    __fitMethod__ = fitting.LevMarLSQFitter()
    __modelImage__ = None

    def __init__(self, FITSfilename=None):
        '''
        Constructor
        
        '''
        if FITSfilename is not None:
            self.__fitsImage__ = (fits.open(path.abspath(FITSfilename)))[0].data
    
        # Gets the image from the file associated with the FITSfilename
        
    def setInitialFit(self,vals):
        '''
        Takes circles as estimates for 
        '''
        self.__vals__ = vals
        self.__wasRun__ = False
    
