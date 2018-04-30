'''
Created on Apr 19, 2018

@author: kaess
'''


import sys
from os import path
from astropy.io import fits
import numpy as np

if __name__ == '__main__':
    """Usage: python3 FlipFits.py <filename.fits>
    output: <filename_edit.fits> with right half of images flipped left-right"""

    inputFilename = path.abspath(sys.argv[1])  # Take first arg as input file
    # open the file as read only- TODO handle case of file not found.
    fitsFile = fits.open(inputFilename)

    # Make an outut filename with '_edit' at the end
    fileNameBits = inputFilename.split('.')
    outputFilename = fileNameBits[0] + '_edit.' + fileNameBits[1]

    # pull the image cube or image
    fitsData = fitsFile[0].data

    shape = np.shape(fitsData)  # get the dimensions of the image data
    width = shape[np.size(shape) - 1]  # get the width of the images
    # get the dimension of the image (n==3 cube, n==2 single)
    n = np.size(shape)
    if n == 3:  # its a cube
        newData = np.concatenate(
            (fitsData[:, :, 0:width // 2], np.flip(fitsData[:, :, width // 2:], 2)), 2)  # flip right half of third axis
    elif n == 2:  # it's a single image
        newData = np.concatenate(
            (fitsData[:, 0:width // 2], np.flip(fitsData[:, width // 2:], 1)), 1)  # flip right half of second axis.
    else:
        print('NOOOOOO! I don\'t know what to do!!!')

    if newData is not None:  # if we flipped things properly
        fitsFile[0].data = newData  # write the new data to the HDU
        fitsFile[0].header[
            'NOTICE'] = 'Post-processed to left-right flip right side of frames'  # Add a header to indicate the modification
        fitsFile[0].writeto(outputFilename)  # write the HDU to the output file

    pass
