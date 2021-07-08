from vtk.util import numpy_support
from vtk import *
# common packages 
import numpy as np 
import os
from math import *
import matplotlib.pyplot as plt
import pydicom
from functools import reduce# reading in dicom files
from matplotlib.widgets import Slider

def load_scan(path):
    slices = [pydicom.dcmread(path + '/' + s) for s in               
              os.listdir(path)]
    slices = [s for s in slices if 'SliceLocation' in s]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices

def get_pixels_value(scans):
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)    # Set outside-of-scan pixels to 0
    
    return np.array(image, dtype=np.int16)

# set path and load files 
path = '/Users/imageens/jy_data/Anon_Study - 0/Myo_PC_Series_25/'
patient_dicom = load_scan(path)
patient_pixels = get_pixels_value(patient_dicom)#sanity check
vtk_data = numpy_support.numpy_to_vtk(num_array=patient_pixels.ravel(), deep=True, array_type=VTK_FLOAT)
imageVTK = vtkImageData()
print(len(patient_pixels))
print((patient_pixels.shape))
imageVTK.SetDimensions(patient_pixels.shape[0],patient_pixels.shape[1],patient_pixels.shape[2])
imageVTK.SetSpacing(1.0, 1.0, 1.0)
imageVTK.SetOrigin(0.0, 0.0, 0.0)
imageVTK.GetPointData().SetScalars(vtk_data)

mapper = vtk.Rendering.Core.vtkMapper;
mapper.setInputData(imageVTK);
actor = vtk.Rendering.Core.vtkActor;
actor.setMapper(mapper);


# cylinderMapper = vtkPolyDataMapper()
# cylinderMapper.SetInputConnection(imageVTK.GetOutputPort())

# idx0 = 0

# l = plt.imshow(patient_pixels[idx0])
# axidx = plt.axes([0.15, 0.02, 0.65, 0.03])
# # axidx = plt.axes()
# slidx = Slider(axidx, 'index', valinit=idx0, valmin=0, valmax=len(patient_pixels) -1, valfmt='%0.0f')
# def update(val):
#     idx = int(slidx.val)
#     print(idx)
#     l.set_data(patient_pixels[idx])
# slidx.on_changed(update)

# plt.show()
