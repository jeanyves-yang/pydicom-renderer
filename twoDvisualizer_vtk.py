import vtk 
import os

path = '/Users/imageens/jy_data/4D FLOW/Amigo 1/Camcmorphv - 3983/4D_Flow_SAG_210/'
# Read data in VTK format
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(path)
reader.Update()


# Start by creating a black/white lookup table.
bw_lut = vtk.vtkLookupTable()
bw_lut.SetTableRange(0, 2000)
bw_lut.SetSaturationRange(0, 0)
bw_lut.SetHueRange(0, 0)
bw_lut.SetValueRange(0, 1)
bw_lut.Build()  # effective built

sagittal_colors = vtk.vtkImageMapToColors()
sagittal_colors.SetInputConnection(reader.GetOutputPort())
sagittal_colors.SetLookupTable(bw_lut)
sagittal_colors.Update()

sagittal = vtk.vtkImageActor()
sagittal.GetMapper().SetInputConnection(sagittal_colors.GetOutputPort())
# sagittal.SetDisplayExtent(128, 128, 0, 255, 0, 92)
sagittal.ForceOpaqueOn()

render = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
render.AddActor(sagittal)
render.SetBackground(255, 255, 255)
renWin.AddRenderer( render )
iren.SetRenderWindow(renWin)
istyle = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(istyle)

iren.Initialize()
iren.Start()
