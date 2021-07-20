# This file implements a direct volume rendering (DVR) using the ray casting method.
# Input path is a folder containing a list of .dcm files, representing a 3D volume.
# Method is implemented using scipy and native python, reader uses

import numpy as np 
import os
from math import *
import matplotlib.pyplot as plt
import pydicom
import scipy.ndimage

from scipy.interpolate import interpn

from time import process_time

def load_scan(path):
    slices = [pydicom.dcmread(path + '/' + s) for s in               
              os.listdir(path)]
    slices = [s for s in slices if 'SliceLocation' in s]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    return slices

def get_pixels_value(scans):
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)    # Set outside-of-scan pixels to 0
    
    return np.array(image, dtype=np.int16)

def transferFunction(x):
    """Transfer Function returns r,g,b,a values as a function of density x"""

    r = 1.0*np.exp( -(x - 21.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
    g = 1.0*np.exp( -(x - 21.0)**2/1.0 ) +  1.0*np.exp( -(x - 3.0)**2/0.1 ) +  0.1*np.exp( -(x - -3.0)**2/0.5 )
    b = 0.1*np.exp( -(x - 21.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) +  1.0*np.exp( -(x - -3.0)**2/0.5 )
    a = 0.6*np.exp( -(x - 21.0)**2/1.0 ) +  0.1*np.exp( -(x - 3.0)**2/0.1 ) + 0.01*np.exp( -(x - -3.0)**2/0.5 )

    return r,g,b,a

# set path and load files 
path = '/Users/imageens/jy_data/Anon_Study - 0/Myo_PC_Series_25/'
patient_dicom = load_scan(path)
patient_pixels = get_pixels_value(patient_dicom)#sanity check


def resample(image, scan, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    spacing = np.array([float(scan[0].SliceThickness), scan[0].PixelSpacing[1],
     scan[0].PixelSpacing[0]])

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    return image, new_spacing

# print("Shape before resampling\t", patient_pixels.shape)
# imgs_after_resamp, spacing = resample(patient_pixels, patient_dicom, [10,10,10])
# print("Shape after resampling\t", imgs_after_resamp.shape)
# print(imgs_after_resamp)

Nangles = 10
t1_start = process_time() 
for i in range(Nangles):
    
    print('Rendering Scene ' + str(i+1) + ' of ' + str(Nangles) + '.\n')

    # Camera Grid / Query Points -- rotate camera view
    angle = np.pi/2 * i / Nangles
    N = 50
    c = np.linspace(-N/2, N/2, N)
    qx, qy, qz = np.meshgrid(c,c,c)
    qxR = qx
    qyR = qy * np.cos(angle) - qz * np.sin(angle) 
    qzR = qy * np.sin(angle) + qz * np.cos(angle)
    qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    
    # Interpolate onto Camera Grid
    # Construct the Corresponding Datacube Grid Coordinates
    Nx, Ny, Nz = patient_pixels.shape
    x = np.linspace(-Nx/2, Nx/2, Nx)
    y = np.linspace(-Ny/2, Ny/2, Ny)
    z = np.linspace(-Nz/2, Nz/2, Nz)
    points = (x, y, z)
    camera_grid = interpn(points, patient_pixels, qi, method='linear').reshape((N,N,N))

    # Do Volume Rendering
    image = np.zeros((camera_grid.shape[1],camera_grid.shape[2],3))

    for dataslice in camera_grid:
        r,g,b,a = transferFunction(np.log(dataslice))
        image[:,:,0] = a*r + (1-a)*image[:,:,0]
        image[:,:,1] = a*g + (1-a)*image[:,:,1]
        image[:,:,2] = a*b + (1-a)*image[:,:,2]
    
    image = np.clip(image,0.0,1.0)
    
    # Plot Volume Rendering
    # plt.figure(figsize=(4,4), dpi=80)
    
    # plt.imshow(image)
    # plt.axis('off')
    # plt.show()
    
    # Save figure
    # plt.savefig('volumerender' + str(i) + '.png',dpi=240,  bbox_inches='tight', pad_inches = 0)

t1_stop = process_time() 

print("Elapsed time in seconds:", t1_stop - t1_start) 

# Plot Simple Projection -- for Comparison
plt.figure(figsize=(4,4), dpi=80)

plt.imshow(np.log(np.mean(patient_pixels,0)), cmap = 'viridis')
plt.clim(-5, 5)
plt.axis('off')

# Save figure
plt.savefig('projection.png',dpi=240,  bbox_inches='tight', pad_inches = 0)
plt.show()

