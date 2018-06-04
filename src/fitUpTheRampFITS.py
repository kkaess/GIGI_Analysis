'''
Created on May 7, 2018

@author: kaess
'''
import os.path as path
from astropy.io import fits

import matplotlib
matplotlib.use('Qt5Agg')
# matplotlib.interactive(True)
from matplotlib import pyplot as plt

import numpy as np

'''
generates weights for least-squares fitting of up-the-ramp data
as per Robberto (2009), for JWST, ignoring secondary effects
'''


def generateWeightsRobberto(n, dt=1.0):
    retVal = np.full(n, 12 / (dt * n * (n * n - 1)), dtype=np.float64)
    for i in np.arange(1, n):
        retVal[i - 1] *= (i - (n + 1) / 2)
    return retVal

'''
takes an np array, array[z,x,y], and least-squares fits up-the-ramp along z
'''


def fitUpTheRampFITS(inputData):
    inputShape = np.shape(inputData)
    weights = generateWeightsRobberto(inputShape[0])
    outputData = np.empty(inputShape[1:])
    for i in np.arange(0, inputShape[1]):
        for j in np.arange(0, inputShape[2]):
            outputData[i, j] = np.dot(inputData[:, i, j], weights)
    return outputData


if __name__ == '__main__':
    fitsFile = fits.open(path.abspath('../fakespots/spot4.fits'))

    outputData1 = fitUpTheRampFITS(fitsFile[0].data[:8, :, :])
    outputData2 = fitUpTheRampFITS(fitsFile[0].data[8:16, :, :])
    outputData3 = fitUpTheRampFITS(fitsFile[0].data[16:24, :, :])
    outputData4 = fitUpTheRampFITS(fitsFile[0].data[24:, :, :])

    outputData = outputData1 + outputData2 + outputData3 + outputData4

    plt.imshow(outputData)
    plt.show()
    pass
