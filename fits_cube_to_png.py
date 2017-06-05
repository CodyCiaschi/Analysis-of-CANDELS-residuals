import numpy as np
from astropy.io import fits
import matplotlib.pylab as plt
import os
import glob
import sys

if len(sys.argv) == 1:
    path = os.getcwd()
elif len(sys.argv) == 2:
    path = sys.argv[1]

filepaths = glob.glob(path + '/*.fits')
print filepaths

for file in filepaths:

    _, tail = os.path.split(file)

    original  = fits.getdata(file, 1)
    model = fits.getdata(file, 2)
    residual = fits.getdata(file, 3)

    fig = plt.figure()

    ax1 = fig.add_subplot(1,3,1)
    ax1.imshow(original, aspect = 2)

    ax2 = fig.add_subplot(1,3,2)
    ax2.imshow(model, aspect = 2)

    ax3 = fig.add_subplot(1,3,3)
    ax3.imshow(residual, aspect = 2)

    _, tail = os.path.split(file)
    name = tail.split('.')

    print name

    image_name = '%s_%s.png' %(name[0],name[1])

    plt.savefig(image_name)
