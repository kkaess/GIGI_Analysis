#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 13:09:10 2018

@author: kaess
"""

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt

from astropy.io import fits

import numpy as np

import sys
import os.path as path

def getAllImages(fileName):
    fullFileName = path.abspath(fileName)
    baseDir = path.dirname(fullFileName)
    prefix = path.splitext(path.split(fullFileName)[1])[0]
    
    fitsData = fits.open(fullFileName)[0].data
    numImages = np.shape(fitsData)[0]
    for i in range(0,numImages):
        plt.imshow(fitsData[i,:,:])
        plt.savefig(path.join(baseDir,prefix)+'Im'+repr(i)+'.png')
    for i in range(1,numImages):
        plt.imshow(np.subtract(fitsData[i,:,:],fitsData[i-1,:,:]))
        plt.savefig(path.join(baseDir,prefix)+'ImSub'+repr(i)+'_'+repr(i-1)+'.png')

if __name__=='__main__':
    for fileName in sys.argv[1:]:
        print(fileName)
        getAllImages(fileName)
