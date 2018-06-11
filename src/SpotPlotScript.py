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

import seaborn as sns

#sns.set()
sns.set_context("poster")


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

mirrorFitLine = np.sum(mirrorFit(x,y),1)
gratingFitLine = np.sum(gratingFit(x,y),1)

gratingScale = 1/gratingFitLine[50]
mirrorScale = 1/mirrorFitLine[50]

x_range = range(0,81)

plt.plot(x_range,np.sum(gratingImageSmall,1)[10:-9]*gratingScale,'ro',label='Grating')
plt.plot(x_range,gratingFitLine[10:-9]*gratingScale,'r-',label='Grating Fit')
plt.plot(x_range,np.sum(mirrorImageSmall,1)[10:-9]*mirrorScale,'bs',label='Mirror')
plt.plot(x_range,mirrorFitLine[10:-9]*mirrorScale,'b-',label='Mirror Fit')
plt.xlabel('Pixel')
plt.ylabel('Normalized Intensities')

plt.xlim(-1,81)
plt.legend()

plt.savefig('ScaledSpotProfiles.png')

plt.close()

fig = plt.figure()

fig, axes = plt.subplots(1,4)

image1 = gratingImageSmall[10:-9,:]*gratingScale
image2 = gratingFit(x,y)[10:-9,:]*gratingScale
image3 = mirrorImageSmall[10:-9,:]*mirrorScale
image4 = mirrorFit(x,y)[10:-9,:]*mirrorScale

imin = min((np.min(image1),np.min(image2),np.min(image3),np.min(image4)))
imax = max((np.max(image1),np.max(image2),np.max(image3),np.max(image4)))


ax = plt.subplot(1,4,1)
ax.imshow(image1,vmin=imin,vmax=imax)
ax.title.set_text('Grating')

ax = plt.subplot(1,4,2)
ax.imshow(image2,vmin=imin,vmax=imax)
ax.title.set_text('Grating Fit')

ax = plt.subplot(1,4,3)
ax.imshow(image3,vmin=imin,vmax=imax)
ax.title.set_text('Mirror')

ax = plt.subplot(1,4,4)
img = ax.imshow(image4,vmin=imin,vmax=imax)
ax.title.set_text('Mirror Fit')


plt.savefig('SpotImagesWithFits.png')


 
