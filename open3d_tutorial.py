import numpy as np
import open3d as o3d
import plotly.graph_objects as go

rabbit_cloud = o3d.io.read_point_cloud("assets/bunny.pcd")
if rabbit_cloud.is_empty(): exit()
rabbit_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

rabbit_mesh = o3d.io.read_triangle_mesh("assets/bunny.obj")

if not rabbit_mesh.has_vertex_normals():
    rabbit_mesh.compute_vertex_normals()
if not rabbit_mesh.has_triangle_normals():
    rabbit_mesh.compute_triangle_normals()


def draw(geometries):
    # Initialize an array for Plotly graph objects
    graph_obj = []
    for gm in geometries:
        # First, determine whether the geometry is point cloud or mesh
        geometry_type = gm.get_geometry_type()
        # If it is point cloud
        if geometry_type == o3d.geometry.Geometry.Type.PointCloud:
            # array to store point coordinates of the point cloud
            pts = np.asarray(gm.points)
            # array to store colors of the point clous
            clr = None  # for colors
            """If the point cloud has point colors, store RGB colors of the point cloud in clr array"""
            if gm.has_colors():
                clr = np.asarray(gm.colors)
                # If the point cloud has point normals, update clr array accordingly
            elif gm.has_normals():
                clr = (0.5, 0.5, 0.5) + np.asarray(gm.normals) * 0.5
            else:
                # Paint each point with the same color first
                gm.paint_uniform_color((1.0, 0.0, 0.0))
                # Update the clr array with point cloud’s colors
                clr = np.asarray(gm.colors)
                # Scatter plot of the point cloud using Plotly
                sc = go.Scatter3d(x=pts[:, 0], y=pts[:, 1], z=pts[:, 2], mode='markers', marker=dict(size=1, color=clr))
                # Add the scatter plot to the graph objects array
                graph_obj.append(sc)
                # If the geometry if the mesh
                if geometry_type == o3d.geometry.Geometry.Type.TriangleMesh:
                    # Store triangles’ coordinates of the mesh
                    tri = np.asarray(gm.triangles)
                    # Store vertices’ coordinates of the mesh
                    vert = np.asarray(gm.vertices)
                    # Initialize the tuple to store colors of the mesh
                    clr = None
                    # if the mesh has triangle normals
                    if gm.has_triangle_normals():
                        clr = (0.5, 0.5, 0.5) + np.asarray(gm.triangle_normals) * 0.5
                        clr = tuple(map(tuple, clr))
                    else:
                        clr = (1.0, 0.0, 0.0)
                    # Define the 3D mesh
                    mesh = go.Mesh3d(x=vert[:, 0], y=vert[:, 1], z=vert[:, 2],
                                     i=tri[:, 0], j=tri[:, 1], k=tri[:, 2], facecolor=clr, opacity=0.50)
                    # Add the mesh to graph objects array
                    graph_obj.append(mesh)
                    # Plot the figure using Plotly
                    fig = go.Figure(data=graph_obj, layout=dict(
                        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False))))
                    fig.show()  # Display the figure


o3d.visualization.draw_geometries = draw  # replace function
# draw the point cloud
o3d.visualization.draw_geometries([rabbit_cloud])
# draw the mesh
o3d.visualization.draw_geometries([rabbit_mesh])
