import open3d as o3d
import numpy as np
import pdb
import json
import os

from carve_voxel import voxel_carving

def read_mesh(path):
    """
    Input: The file path to the object.
    Output: The open3d mesh object of the object with computed vert4ex normals 
    """
    if __name__ == "__main__":
        print("Testing mesh in open3d ...")
        mesh = o3d.io.read_triangle_mesh(path)#here one maybe needs to change the data path of the input data
        print(mesh)
        #print(np.asarray(mesh.vertices))
        #print(np.asarray(mesh.triangles))
        print("")
        mesh.compute_vertex_normals()
        return(mesh)


def voxelizer(mesh_path, scale, size, gap):
    """
    scale: the scale of bounding box of mesh
    size: the size of cubic
    gap: the number of cubic between the interior and surface.

    """
    mesh = read_mesh(mesh_path)
    mesh.scale(scale / np.max(mesh.get_max_bound() - mesh.get_min_bound()),center=mesh.get_center())
    voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh,voxel_size=size)
    N_axis = int(scale / size)
    voxel_matrix = np.zeros((N_axis,N_axis,N_axis))
    #pdb.set_trace()
    center_point = voxel_grid.get_center()
    center_index = voxel_grid.get_voxel(center_point)
    print("center point",center_point)
    print("center_index",center_index)
    
    for i in voxel_grid.get_voxels(): # index is from 1 to scale/size
        #print(i.grid_index)
        a = i.grid_index #a[0] a[1] a[2]
        voxel_matrix[a[0]-1,a[1]-1,a[2]-1] = 1
    print("before fill=",voxel_matrix.sum())
    before_voxel = voxel_matrix

    print("after fill = ", voxel_matrix.sum())
    #o3d.visualization.draw_geometries([voxel_grid])
    #pdb.set_trace()
    voxel = { 
        "mesn_file" : mesh_path,
        "center_point" : center_point.tolist(), 
        "center_index": center_index.tolist(),
        "scale" : scale, 
        "size": size,
        "gap" : gap, 
        "voxel_matrix" : np.array(voxel_matrix, dtype=bool).tolist()
    } 
    return voxel

mesh_path = "./data/bunny.obj"
mesh = o3d.io.read_triangle_mesh(mesh_path)
output_filename = os.path.abspath("./data/voxelized.ply")
camera_path = os.path.abspath("./data/sphere.ply")
visualization = True
cubic_size = 2.0
voxel_resolution = 64.0

voxel_grid, voxel_carving, voxel_surface = voxel_carving(
    mesh, output_filename, camera_path, cubic_size, voxel_resolution)

open3d.io.write_voxel_grid(output_filename,voxel_grid)


import pdb
pdb.set_trace()

print("surface voxels")
print(voxel_surface)
o3d.visualization.draw_geometries([voxel_surface])

print("carved voxels")
print(voxel_carving)
o3d.visualization.draw_geometries([voxel_carving])

print("combined voxels (carved + surface)")
print(voxel_grid)
o3d.visualization.draw_geometries([voxel_grid])


#voxel = voxelizer(mesh_path, 10, 0.5, 2)
## the length of bounding box is 1/0.05=20


#file_name = "./data/voxel.json"

#with open(file_name, "w", encoding='utf-8') as f:
#    #json.dump(voxel_matrix.tolist(),f,separators=(',', ':'))
#    json.dump(voxel, f, indent=4)
