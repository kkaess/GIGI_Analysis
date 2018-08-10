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

from matplotlib import cm
from matplotlib.pyplot import imshow

from PIL import Image

def frame(hdul, n):
    """Returns the n-th frame of the primary hdu in the passed hdul"""
    return hdul[0].data[n,:,:]

def diff(hdul, frame1, frame2):
    return np.subtract(frame(hdul, frame1),frame(hdul,frame2))

def imshowFrame(hdul,frame_):
    imshow(frame(hdul,frame_))
    
def imshowStretch(hdul,frame_,min_,max_):
    imshow(np.clip(frame(hdul,frame_),min_,max_))
    
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
    firstFiveColumns = np.sum(image2D,0)[0:5]
    if firstFiveColumns[0]>np.average(firstFiveColumns):
        return fixFlipped(image2D)
    else:
        return flipRHS(image2D)


def fixFlipped(image2D):
    return np.flip(flipRHS(fixLeftOffByOne(image2D)),1)

def convertImage(frame_, cm_=cm.viridis):
    return Image.fromarray(np.uint8(cm_(np.interp(frame_, (frame_.min(), frame_.max()), (0, 1))) * 255))

def getComment(hdul_):
    return hdul_[0].header['COMMENT']
