'''
Created on Jul 15, 2018

@author: kaess
'''

import warnings

import os.path as path
from astropy.io.fits.hdu.hdulist import HDUList
import numpy as np


class GIGIFits(HDUList):
    '''
    classdocs
    '''

    def __init__(self, filename=None):
        '''
        Constructor
        '''
        if filename is not None:
            super().__init__(file=open(path.abspath(filename), 'rb'))
        else:
            super().__init__()
            
        self.__frames__ = np.size(self[0].data,0)
        self.__cvFrames__ = [None]*self.__frames__
        self.__rampFit__ = None
    
    def __repr__(self):
        '''
        Object identification
        overloaded because HDUList repr hangs when called from this object
        '''
        return object.__repr__(self)
    
    def n(self):
        return self.__frames__
    
    def frame(self, n):
        return self[0].data[n, :, :]
    
    def cvFrame(self, n):
        '''
        returns the n-th frame scaled to unsigned 8-bit precision
        '''
        if self.__cvFrames__[n] is None:
            frame = self.frame(n)
            self.__cvFrames__[n] = np.uint8(np.interp(frame, (np.min(frame), np.max(frame)), (0, 1)) * 255)
        return self.__cvFrames__[n]
        
    def rampFit(self):
        if self.__rampFit__ is None:
            n = n = np.size(self[0].data, 0)
            sum_t = n * (n + 1) / 2
            sum_tsq = n * (n + 1) * (2 * n + 1) / 6
    
            ti = np.arange(1, n + 1)
    
            sum_s = np.sum(self[0].data, 0)
            sum_ts = np.dot(np.swapaxes(np.swapaxes(self[0].data, 0, 2), 0, 1), ti)
    
            denominator = n * sum_tsq - sum_t ** 2
    
            b = (n * sum_ts - sum_t * sum_s) / denominator
            a = (sum_tsq * sum_s - sum_t * sum_ts) / denominator
    
            self.__rampFit__ = [a, b]
        return self.__rampFit__
    
    def cvRampFit(self):
        if self.__rampfit__ is None:
            self.rampFit()
        return np.uint8(np.interp(self.__rampFit__, (np.min(self.__rampFit__), np.max(self.__rampFit__)), (0, 1)) * 255)
    
