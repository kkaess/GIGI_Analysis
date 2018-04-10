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

    def __init__(self):
        self.center = 0
        self.std_dev = 0

    def callback(self, event):
        (x1, y1), (x2, y2) = pyplot.ginput(2, timeout=0, show_clicks=True)
        self.center = (x1, y1)
        self.std_dev = ((x1 - x2)**2 + (y1 - y2)**2)**0.5


if __name__ == '__main__':
    fitsFile = fits.open(os.path.abspath('../fakespots/spot1.fits'))
    fitsImage = fitsFile[0].data

    # this will be user selected eventually
    fitEstimate = models.Gaussian2D(
        amplitude=100, x_mean=550, y_mean=632, x_stddev=3, y_stddev=3)
    fitEstimate2 = models.Gaussian2D(
        amplitude=10, x_mean=421, y_mean=778, x_stddev=3, y_stddev=3)
    fitMethod = fitting.LevMarLSQFitter()
    y, x = np.mgrid[:1024, :1024]
    fitModel = fitMethod(fitEstimate + fitEstimate2, x, y, fitsImage)
    print(fitModel[0].parameters)
    print(fitModel[1].parameters)

    print(repr(fitModel))
    modelImage = fitModel(x, y)

    pyplot.figure(figsize=(8, 2.5))

    ax1 = pyplot.subplot(1, 3, 1)
    pyplot.imshow(fitsImage, origin='lower', interpolation='nearest')
    pyplot.title("Data")
    pyplot.subplot(1, 3, 2, sharex=ax1, sharey=ax1)
    pyplot.imshow(modelImage, origin='lower', interpolation='nearest')
    pyplot.title("Model")
    pyplot.subplot(1, 3, 3, sharex=ax1, sharey=ax1)
    pyplot.imshow(fitsImage - modelImage, origin='lower',
                  interpolation='nearest')
    pyplot.title("Residual")
    pyplot.colorbar(extend='both')
    # This to be implemented later
    #axwhat = pyplot.axes([0.7, 0.05, 0.1, 0.075])
    #button = Button(axwhat, 'Select Spot')

    pyplot.show()

    pass
