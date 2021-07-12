import vtk 
import os

path = '/Users/imageens/jy_data/Anon_Study - 0/Myo_PC_Series_25/'
for filename in os.listdir(path):
    reader = vtk.vtkDICOMImageReader()
    reader.SetFileName(path + filename)
    reader.Update()

    dataset = reader.GetOutput()
    array = dataset.GetPointData().GetScalars()
    mini, maxi = array.GetFiniteRange()

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(dataset)
    mapper.GetLookupTable().SetNumberOfTableValues(256)
    mapper.SetScalarRange(mini, maxi)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToSurface()
    actor.GetProperty().LightingOff()

    render = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()
    render.AddActor(actor)
    render.SetBackground(255, 255, 255)
    renWin.AddRenderer( render )
    iren.SetRenderWindow(renWin)
    istyle = vtk.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(istyle)

    iren.Initialize()
    iren.Start()