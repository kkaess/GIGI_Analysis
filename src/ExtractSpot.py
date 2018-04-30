'''
Created on Apr 24, 2018

@author: kaess
'''

import sys
import os.path as path

from astropy.io import fits
import numpy as np

if __name__ == '__main__':
    imageFilename = sys.argv[1]
    backgroundFilename = sys.argv[2]
    if imageFilename is None or backgroundFilename is None:
        print('Usage: FlipFits.py <image> <background> -> output: <image - background>')
        pass

    fileNameBits = imageFilename.split('.')
    outputFilename = fileNameBits[0] + '_subtracted.' + fileNameBits[1]

    imageFile = fits.open(path.abspath(imageFilename))
    backgroundFile = fits.open(path.abspath(backgroundFilename))

    image = np.sum(imageFile[0].data, 0)
    background = np.sum(backgroundFile[0].data, 0)

    newHDU = imageFile[0].copy()
    newHDU.data = np.subtract(image, background)
    newHDU.writeto(outputFilename)

    pass
