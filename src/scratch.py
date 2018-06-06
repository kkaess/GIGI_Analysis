#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 01:24:22 2018

@author: kaess
"""


import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.interactive(True)

import numpy as np

from matplotlib.pyplot import imshow as show

def frame(hdul, frame):
    return hdul[0].data[frame,:,:]

def diff(hdul, frame1, frame2):
    return np.subtract(frame(hdul, frame1),frame(hdul,frame2))

def showFrame(hdul,frame_):
    show(frame(hdul,frame_))
    
def showStretch(hdul,frame_,min,max):
    show(np.clip(frame(hdul,frame_),min,max))
    
def flipRHS(image2D):
    width = np.shape(image2D)[1]
    return np.concatenate(
            (image2D[ :, 0:width // 2], np.flip(image2D[ :, width // 2:], 1)), 1)
    
def fixOffByOne(imageHalf):
    firstColumn = np.concatenate((imageHalf[1:,0:1],imageHalf[0:1,0:1]),0)
    return np.concatenate((imageHalf[:,1:],firstColumn),1)

def fixLeftOffByOne(image2D):
    width = np.shape(image2D)[1]
    return np.concatenate((fixOffByOne(image2D[:,:width//2]),image2D[:,width//2:]),1)

def fix(image2D):
    return flipRHS(image2D)

def fixFlipped(image2D):
    return np.flip(flipRHS(fixLeftOffByOne(image2D)),1)
