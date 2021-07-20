import pyvista as pv
from pyvista import examples
import numpy as np

anatomy = pv.read('/Users/imageens/imageenslibrary_python/imageens/Data/triggertime_331/triggertime_331.vti')
flow_x = pv.read('/Users/imageens/imageenslibrary_python/imageens/Data/triggertime_x_331/triggertime_x_331.vti')
flow_y = pv.read('/Users/imageens/imageenslibrary_python/imageens/Data/triggertime_y_331/triggertime_y_331.vti')
flow_z = pv.read('/Users/imageens/imageenslibrary_python/imageens/Data/triggertime_z_331/triggertime_z_331.vti')

# Flow in 2x is actually antero posterior axis (X as we loaded sagittal just like axial ..)
# Flow in y is left right (Z)
# Flow in z is top down (Y)

# flow_x = flow_x.threshold(0.2)
# flow_y = flow_y.threshold(0.2)
# flow_z = flow_z.threshold(0.2)

flow = np.concatenate(
    (flow_x.active_scalars.reshape(flow_x.active_scalars.shape[0],1),
    flow_z.active_scalars.reshape(flow_y.active_scalars.shape[0],1),
    flow_y.active_scalars.reshape(flow_z.active_scalars.shape[0],1)), axis=1)
anatomy.point_arrays["flow"] = flow

thresholded = anatomy.threshold((70, 255))

# print(flow.shape)
# print(anatomy)
# print(flow_x.active_scalars)
# print(flow_x)
# print(flow_y)
# print(flow_z)
# print(thresholded)
# print(thresholded.array_names)
# streamlines method requires a velocity field, it can be any name, as a point array, size (n_points, 3)
# anatomy.save("/Users/imageens/imageenslibrary_python/imageens/Data/triggertime_331_with_xzyflow.vti")
streamlines, src = thresholded.streamlines(
    return_source=True,
    max_time=100.0,
    initial_step_length=1.0,
    terminal_speed=0.1,
    n_points=10000,
    source_radius=60.0,
    source_center=(80.0, 358.0, 42.0),
)

# print(streamlines)
# streamlines = thresholded.streamlines(
#     max_time=100.0,
#     initial_step_length=2.0,
#     terminal_speed=0.1,
#     start_position=thresholded.points[1000],
# )

# streamlines = thresholded.streamlines_from_source(thresholded.threshold(0.5))
# print(mesh)
# print(streamlines)

# # p.add_mesh(mesh.outline(), color="k")
# p.add_mesh(streamlines.tube(radius=0.15))
# p.add_mesh(src)
# p.add_mesh(mesh, cmap="bone", volume=True)
# # p.add_mesh(mesh.contour([160]).extract_all_edges(), color="grey", opacity=0.25)
# p.camera_position = [(182.0, 177.0, 50), (139, 105, 19), (-0.2, -0.2, 1)]
# p.show()

# mesh = examples.download_carotid()
# print(mesh.point_arrays)
# mesh.set_active_scalars("vectors")
# print(mesh)
# print(len(mesh.points))

# mesh = examples.download_blood_vessels().cell_data_to_point_data()
# mesh.set_active_scalars("velocity")
# print(mesh.array_names)
# print(mesh.active_scalars_name)
# print(mesh.active_vectors_name)
# print(mesh.get_array("vectors").shape)
# print(mesh.points)


# streamlines, src = mesh.streamlines(
#     return_source=True,
#     max_time=100.0,
#     initial_step_length=2.0,
#     terminal_speed=0.1,
#     n_points=25,
#     source_radius=2.0,
#     source_center=(133.1, 116.3, 5.0),
# )

# print(streamlines)
# print(mesh.points)
# print(thresholded.points[1000])
# print(src)


p = pv.Plotter()
p.add_mesh(thresholded.outline(), color="k")
# p.add_mesh(thresholded)
p.add_mesh(streamlines.tube(radius=0.1), opacity=255)
# p.add_mesh(src)
p.add_mesh(thresholded.contour([70]).extract_all_edges(), color="grey", opacity=0.25)
# p.camera_position = [(182.0, 177.0, 50), (139, 105, 19), (-0.2, -0.2, 1)]
p.show_axes()
p.show()