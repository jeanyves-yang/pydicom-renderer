# This file implements an indirect volume rendering (IDVR) using the marching cubes method.
# Input path is a folder containing a list of .dcm files, representing a 3D volume.
# Method is implemented using plotly, reader uses pydicom.

import numpy as np 
import os
from math import *
import matplotlib.pyplot as plt
import pydicom
import scipy.ndimage

from plotly import __version__
from plotly import figure_factory as FF
from plotly.graph_objs import *

from skimage import measure

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

print("Shape before resampling\t", patient_pixels.shape)
imgs_after_resamp, spacing = resample(patient_pixels, patient_dicom, [10,10,10])
print("Shape after resampling\t", imgs_after_resamp.shape)

def make_mesh(image, threshold=21, step_size=1):

    print("Transposing surface")
    p = image.transpose(2,1,0)
    
    print("Calculating surface")
    
    verts, faces, norm, val = measure.marching_cubes(p, threshold, step_size=step_size, allow_degenerate=True) 

    return verts, faces

def plotly_3d(verts, faces):
    x,y,z = zip(*verts) 
    
    print("Drawing")
    
    # Make the colormap single color since the axes are positional not intensity. 
#    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
    colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']
    
    fig = FF.create_trisurf(x=x,
                        y=y, 
                        z=z, 
                        plot_edges=False,
                        colormap='Viridis',
                        simplices=faces,
                        backgroundcolor='rgb(64, 64, 64)',
                        title="Interactive Visualization")

                        
    fig.show()

def plt_3d(verts, faces):
    print("Drawing")
    x,y,z = zip(*verts) 
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
    face_color = [1, 1, 0.9]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_zlim(0, max(z))
    ax.set_facecolor((0.7, 0.7, 0.7))
    plt.show()

v, f = make_mesh(patient_pixels, 50, 1)
plotly_3d(v, f)

# plt.hist(imgs_after_resamp.flatten(), bins=50, color='c')
# plt.show()
