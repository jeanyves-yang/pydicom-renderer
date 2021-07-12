from vtk.util import numpy_support
import vtk
import os
import math
from functools import reduce

# set path and load files 
path = '/Users/imageens/jy_data/4DFlow_testData/4D_anatomic/'
test = 0

for filename in os.listdir(path):
    if test == 0:
        test = 1
        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName(path + filename)
        reader.Update()

        mapperVolume = vtk.vtkGPUVolumeRayCastMapper()
        mapperVolume.SetInputConnection(reader.GetOutputPort())

        scalarOpacity = vtk.vtkPiecewiseFunction()
        for x in range(0, 8):
            scalarOpacity.AddPoint(x * 8, x / 8)

        propVolume = vtk.vtkVolumeProperty()
        
        color = vtk.vtkColorTransferFunction()
        color.AddRGBPoint(0, 0.23, 0.29, 0.75)
        color.AddRGBPoint(0.48, 0.86, 0.86, 0.86)
        color.AddRGBPoint(0.96, 0.70, 0.01, 0.14)
        range = reader.GetOutput().GetPointData().GetScalars().GetRange()
        color.SetRange(range)

        sampleDistance = 0.7 * math.sqrt(
            reduce(lambda a,b: a+b,
            map(lambda v: v * v, reader.GetOutput().GetSpacing())))

        mapperVolume.SetSampleDistance(sampleDistance)
        mapperVolume.Update()

        gradientOpacity = vtk.vtkPiecewiseFunction()
        gradientOpacity.AddPoint(0, 0.0)
        print((range[1] - range[0]) * 0.05)
        gradientOpacity.AddPoint(0, (range[1] - range[0]))

        propVolume.SetInterpolationTypeToLinear()
        propVolume.ShadeOn()
        propVolume.SetAmbient(0.2)
        propVolume.SetDiffuse(0.7)
        propVolume.SetSpecular(0.3)
        propVolume.SetSpecularPower(8.0)

        propVolume.SetScalarOpacity(scalarOpacity)
        propVolume.SetGradientOpacity(gradientOpacity)
        propVolume.SetColor(color)

        volume = vtk.vtkVolume()
        volume.SetMapper(mapperVolume)
        volume.SetProperty(propVolume)
        volume.Update()

        render = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        iren = vtk.vtkRenderWindowInteractor()
        # render.AddActor(actor)
        render.AddVolume(volume)
        render.SetBackground(255, 255, 255)
        renWin.AddRenderer( render )
        iren.SetRenderWindow(renWin)
        istyle = vtk.vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(istyle)

        iren.Initialize()
        iren.Start()

        # print(mapperVolume.GetLastUsedRenderMode())

