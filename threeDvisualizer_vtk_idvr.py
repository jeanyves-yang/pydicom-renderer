from vtk.util import numpy_support
import vtk
import os

# set path and load files 
path = '/Users/imageens/jy_data/4DFlow_testData/4D_anatomic/'
test = 0

colors = vtk.vtkNamedColors()
# Set the background color.
bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
colors.SetColor("BkgColor", *bkg)

for filename in os.listdir(path):
    if test == 0:
        test = 1
        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName(path + filename)

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        mapper.Update()


        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
        actor.RotateX(30.0)
        actor.RotateY(-45.0)

        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # Add the actors to the renderer, set the background and size
        ren.AddActor(actor)
        ren.SetBackground(colors.GetColor3d("BkgColor"))
        renWin.SetSize(300, 300)
        renWin.SetWindowName('CylinderExample')

        # This allows the interactor to initalize itself. It has to be
        # called before an event loop.
        iren.Initialize()

        # We'll zoom in a little by accessing the camera and invoking a "Zoom"
        # method on it.
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.5)
        renWin.Render()

        # Start the event loop.
        iren.Start()