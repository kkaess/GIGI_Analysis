'''
Created on Apr 9, 2018

@author: kaess
'''
import os

from astropy.io import fits

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot
from matplotlib.widgets import Button

import numpy as np

from astropy.modeling import models, fitting


class GuessValues(object):
    center = 0
    std_dev = 0

    def hollaback(self, event):
        (x1, y1), (x2, y2) = pyplot.ginput(2, timeout=0, show_clicks=True)
        self.center = (x1, y1)
        self.std_dev = ((x1 - x2)**2 + (y1 - y2)**2)**0.5


if __name__ == '__main__':
    fitsFile = fits.open(os.path.abspath('../fakespots/spot1.fits'))
    fitsImage = fitsFile[0].data

    pyplot.figure(figsize=(8, 2.5))
    ax1 = pyplot.subplot(1, 3, 1)
    pyplot.imshow(fitsImage, origin='lower', interpolation='nearest')
    pyplot.title("Data")
    pyplot.subplot(1, 3, 2, sharex=ax1, sharey=ax1)
    pyplot.imshow(fitsImage, origin='lower', interpolation='nearest')
    pyplot.title("Model")
    pyplot.subplot(1, 3, 3, sharex=ax1, sharey=ax1)
    pyplot.imshow(fitsImage, origin='lower', interpolation='nearest')
    pyplot.title("Residual")

    axwhat = pyplot.axes([0.7, 0.05, 0.1, 0.075])
    button = Button(axwhat, 'Select Spot')
    button
    pyplot.show()
    input('Zoom in on a spot and press enter when ready')

    happy = 'n'

    while happy is not 'y':
        happy = input('Are you happy?\n')

    pass
