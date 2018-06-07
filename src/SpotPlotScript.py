#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 11:18:21 2018

@author: kaess
"""

from astropy.io import fits
from astropy.modeling import models, fitting
import numpy as np

import scratch
from scratch import *

from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] =[19.2,10.8]

dark202 = fits.open('/run/media/kaess/ResearchBackup1/FITS Files/2018_05_22/dark202/Picture_1/Frame_1.fits')
laser202 = fits.open('/run/media/kaess/ResearchBackup1/FITS Files/2018_05_22/laser202/Picture_1/Frame_1.fits')

focus7 = fits.open('/run/media/kaess/ResearchBackup1/FITS Files/2018_05_18/focus7/Picture_1/Frame_1.fits')
focus8 = fits.open('/run/media/kaess/ResearchBackup1/FITS Files/2018_05_18/focus8/Picture_1/Frame_1.fits')

mirrorImageSmall = fixFlipped(np.subtract(frame(focus7,3),frame(focus8,3)))[457:557,276:316]
gratingImageSmall = fix(np.subtract(frame(laser202,0),frame(dark202,0)))[256:356,199:239]


fitMethod = fitting.LevMarLSQFitter()
fitEstimateGrating = models.Gaussian2D(amplitude=2.2,x_mean=20,y_mean=50,x_stddev=5,y_stddev=5)
fitEstimateGrating += models.Gaussian2D(amplitude=.6,x_mean=23,y_mean=61,x_stddev=3,y_stddev=3)
fitEstimateGrating += models.Gaussian2D(amplitude=.4,x_mean=28,y_mean=37,x_stddev=3,y_stddev=3)

fitEstimateMirror = models.Gaussian2D(amplitude=.85,x_mean=20,y_mean=50,x_stddev=3,y_stddev=3)
fitEstimateMirror += models.Gaussian2D(amplitude=.17,x_mean=23,y_mean=61,x_stddev=2,y_stddev=2)
fitEstimateMirror += models.Gaussian2D(amplitude=.1,x_mean=27,y_mean=35,x_stddev=2,y_stddev=2)

y,x = np.mgrid[:100,:40]
gratingFit = fitMethod(fitEstimateGrating,x,y,gratingImageSmall)
mirrorFit = fitMethod(fitEstimateGrating,x,y,mirrorImageSmall)

mirrorScale = 3.71

plt.plot(np.sum(gratingImageSmall,1),linestyle='',marker='o')
plt.plot(np.sum(mirrorImageSmall,1)*mirrorScale,linestyle='',marker='s')
plt.plot(np.sum(mirrorFit(x,y),1)*mirrorScale)
plt.plot(np.sum(gratingFit(x,y),1))

plt.savefig('ScaledSpotProfiles.png')

plt.close()

plt.subplot(1,4,1)
plt.imshow(gratingImageSmall)
plt.subplot(1,4,2)
plt.imshow(gratingFit(x,y))
plt.subplot(1,4,3)
plt.imshow(mirrorImageSmall)
plt.subplot(1,4,4)
plt.imshow(mirrorFit(x,y))


plt.savefig('SpotImagesWithFits.png')


 
