'''
Created on Apr 24, 2018

@author: kaess
'''

import sys
import os.path as path

from astropy.io import fits

'''
And another kludge-y script: 
just grabs the string in the COMMMENT of the first HDU of the fits file
outputs it to stdout
'''

if __name__ == '__main__':
    ff = fits.open(path.abspath(sys.argv[1]))
    print(ff[0].header['COMMENT'])
    pass