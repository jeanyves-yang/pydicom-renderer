import vtk

reader = vtk.vtkXMLImageDataReader()

for x in range(0, 49):
    print(x)
    reader.SetFileName("../jy_data/4DFlow_testData/4D_anatomic/0" + str(x) + ".vti")
    reader.Update()
    image = reader.GetOutput()
    writer = vtk.vtkDataSetWriter()
    writer.SetFileName("../jy_data/4DFlow_testData/4D_anatomic_vtk/0" + str(x) + ".vtk")
    writer.SetInputData(image)
    writer.Write()