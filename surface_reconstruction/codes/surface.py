import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import os

# Function to quickly generate Levels of Details (LoD)
def lod_mesh_export(mesh, lods, extension, path):
    mesh_lods={}
    for i in lods:
        mesh_lod = mesh.simplify_quadric_decimation(i)
        #o3d.io.write_triangle_mesh(path+"lod_"+str(i)+extension, mesh_lod)
        mesh_lods[i]=mesh_lod
    print("generation of "+str(i)+" LoD successful")
    return mesh_lods

# Step 2: Load and prepare the data

# PATHS HANDLE
cwd = os. getcwd().split('/')

if cwd[-1] == "PG":
    input_path  = "surface_reconstruction/point_cloud_input/"
    output_path = "surface_reconstruction/output/"

elif cwd[-1] == "surface_reconstruction":
    input_path  = "point_cloud_input/"
    output_path = "output/"

else:
    input_path  = "../point_cloud_input/"
    output_path = "../output/"

# Create variable that hold data name
dataname    = "goku.xyz"

# Load point cloud data
pcd = o3d.io.read_point_cloud(input_path+dataname)
# Quick visual of what was loaded
o3d.visualization.draw_geometries([pcd])
# Downsample pcd data
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
# Quick visual of what was sampled
o3d.visualization.draw_geometries([downpcd])

# Estimate normals
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
# Quick visual Point Clouds with Normals
o3d.visualization.draw_geometries([pcd])
o3d.visualization.draw_geometries([downpcd])

# Step 4: Process the data

# Strategy 1: BPA

# Compute the necessary radius parameter based on the average

# distances computed from all the distances between points for pcd
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist
# distances computed from all the distances between points for downpcd
distances2 = downpcd.compute_nearest_neighbor_distance()
avg_dist2 = np.mean(distances2)
radius2 = 3 * avg_dist2

# Then create a mesh and store it in the bpa_mesh variable
bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))
bpa_mesh.compute_vertex_normals()
bpa_mesh2 = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(downpcd,o3d.utility.DoubleVector([radius, radius * 2]))
bpa_mesh2.compute_vertex_normals()

# We can downsample the result to an acceptable number of triangles,
# for example, 100k triangles:
#dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)

# if you think the mesh can present some weird artifacts,
# you can run the following commands to ensure its consistency
#dec_mesh.remove_degenerate_triangles()
#dec_mesh.remove_duplicated_triangles()
#dec_mesh.remove_duplicated_vertices()
#dec_mesh.remove_non_manifold_edges()

# Strategy 2: Poisson reconstruction

# You just have to adjust the parameters that you pass to
# the function as described above
poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9, width=0,scale=2, linear_fit=False)[0]
poisson_mesh.compute_vertex_normals()

# he function output a list composed of an o3d.geometry object
# followed by a Numpy array. You want to select only the o3d.geometry
# justifying the [0] at the end.

# To get a clean result, it is often necessary to add a cropping
# step to clean unwanted artifacts. For this, we compute the initial
# bounding-box containing the raw point cloud, and we use it to filter
# all surfaces from the mesh outside the bounding-box.
bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = poisson_mesh.crop(bbox)

# Step 5: Export and visualize

#o3d.io.write_triangle_mesh(output_path+"open3d/bpa_mesh.ply", pcl)
#o3d.io.write_triangle_mesh(output_path+"p_mesh_c.ply", p_mesh_crop)
#my_lods = lod_mesh_export(bpa_mesh, [100000,50000,10000,1000,100], ".ply", output_path)
#o3d.visualization.draw_geometries([my_lods[100]])

o3d.visualization.draw_geometries([bpa_mesh])
o3d.visualization.draw_geometries([bpa_mesh2])
o3d.visualization.draw_geometries([p_mesh_crop])