from vtk.util import numpy_support
import vtk
import os
import math
from functools import reduce

from time import process_time

def get_prop_volume():
        propVolume = vtk.vtkVolumeProperty()

        scalarOpacity = vtk.vtkPiecewiseFunction()
        for x in range(0, 8):
            scalarOpacity.AddPoint(x * 8, x / 8)

        color = vtk.vtkColorTransferFunction()
        color.AddRGBPoint(0, 0.23, 0.29, 0.75)
        color.AddRGBPoint(0.48, 0.86, 0.86, 0.86)
        color.AddRGBPoint(0.96, 0.70, 0.01, 0.14)
        dataRange = reader.GetOutput().GetPointData().GetScalars().GetRange()
        color.SetRange(dataRange)

        sampleDistance = 0.7 * math.sqrt(
            reduce(lambda a,b: a+b,
            map(lambda v: v * v, reader.GetOutput().GetSpacing())))

        mapperVolume.SetSampleDistance(sampleDistance)
        mapperVolume.Update()

        gradientOpacity = vtk.vtkPiecewiseFunction()
        gradientOpacity.AddPoint(0, 0.0)
        gradientOpacity.AddPoint(0, (dataRange[1] - dataRange[0]))

        propVolume.SetInterpolationTypeToLinear()
        propVolume.ShadeOn()
        propVolume.SetAmbient(0.2)
        propVolume.SetDiffuse(0.7)
        propVolume.SetSpecular(0.3)
        propVolume.SetSpecularPower(8.0)

        propVolume.SetScalarOpacity(scalarOpacity)
        propVolume.SetGradientOpacity(gradientOpacity)
        propVolume.SetColor(color)

        return propVolume

# set path and load files 
path = '/Users/imageens/jy_data/4DFlow_testData/4D_anatomic/'
test = 0

for filename in os.listdir(path):
    if test == 0:
        test = 1
        t1_start = process_time() 

        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName(path + filename)
        reader.Update()
        print(reader.GetOutput().GetDimensions())
        print(reader.GetOutput().GetNumberOfPoints())

        print(reader.GetOutput().GetPoint(17202320)[0],
        reader.GetOutput().GetPoint(17202320)[1],
        reader.GetOutput().GetPoint(17202320)[2])


        mapperVolume = vtk.vtkFixedPointVolumeRayCastMapper()
        mapperVolume.SetInputConnection(reader.GetOutputPort())

        propVolume = get_prop_volume()

        volume = vtk.vtkVolume()
        volume.SetMapper(mapperVolume)
        volume.SetProperty(propVolume)
        volume.Update()

        seed = vtk.vtkPointSource()
        seed.SetRadius(100)
        seed.SetNumberOfPoints(1000)
        # seed.SetCenter((1.3, 239.0, 447.0))
        seed.SetCenter((0.0, 0.0, 0.0))

        streamTracer = vtk.vtkStreamTracer()
        streamTracer.SetInputConnection(reader.GetOutputPort())
        streamTracer.SetMaximumPropagation(500)
        streamTracer.SetIntegrator(vtk.vtkRungeKutta45())
        streamTracer.SetIntegrationDirectionToBoth()
        streamTracer.SetTerminalSpeed(0.0001)
        streamTracer.SetSourceConnection(seed.GetOutputPort())

        streamMapper = vtk.vtkPolyDataMapper()
        streamMapper.SetInputConnection(streamTracer.GetOutputPort())
        streamMapper.ScalarVisibilityOff()

        streamActor = vtk.vtkActor()
        streamActor.GetProperty().SetColor((0.4, 0.4, 0.4))
        streamActor.SetMapper(streamMapper)
        streamActor.GetProperty().SetOpacity(0.4)


        render = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        iren = vtk.vtkRenderWindowInteractor()
        render.AddVolume(volume)
        render.AddActor(streamActor)
        render.SetBackground(0.1, 0.1, 0.1)
        renWin.AddRenderer( render )
        iren.SetRenderWindow(renWin)
        istyle = vtk.vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(istyle)

        iren.Initialize()
        iren.Start()
        t1_stop = process_time() 

        print("Elapsed time in seconds:", t1_stop - t1_start) 


