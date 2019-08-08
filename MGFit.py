'''
Created on Jul 10, 2019

@author: kaess
'''

from astropy.io import fits
import numpy as np

class MGFit(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        try:
            self.__filehandle__ = fits.open(filename)
        except FileNotFoundError as e:
            print('File not found in MGFit.__init__')
            raise e
        
        self.__data__ = self.__filehandle__[0].data
        if 
