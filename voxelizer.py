import open3d as o3d
import numpy as np
import pdb
import json
import os
import pdb
import copy
from scipy.sparse import csr_matrix

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


def voxel_to_numpy(voxels, voxel_resolution = 64):
    """
    Input: An instance if the open3d voxelgrid datastructure, the number of voxels per sidelength (voxel_resolution)
    Output: A numpy array of voxel_resolution x voxel_resolution x voxel_resolution with 1 and 0, where ever we have a voxel or not 
    """
    vx_numpy = np.zeros((voxel_resolution,voxel_resolution,voxel_resolution))
    grid = voxels.get_voxels()
    for i in grid: # index is from 1 to scale/size
        #print(i.grid_index)
        voxel_index = i.grid_index #a[0] a[1] a[2]
        vx_numpy[voxel_index[0]-1,voxel_index[1]-1,voxel_index[2]-1] = 1
    return vx_numpy

def voxel_surface_numpy(voxels_np):
    """
    Input: 
        voxels: An N x N x N numpy array that indicates the voxel indices of a filled mesh. 
                The values \in \{0,1\}
        thickness: the number of cubes, that should be the thickness of the boundary the voxel grid

    Output: 
        voxels_surface_np, voxels_interior_np . Two numpy arrays that have the same shape as voxels_np. The first one contains the voxels, that are in the surface, the second one contains the voxels, that are in the interior.
        In theory the sum of these two arrays should yield the input array again
    """
    grid_shape = voxels_np.shape
    voxels_int = copy.deepcopy(voxels_np)
    voxel_surface = np.zeros_like(voxels_np)
    #somehow a sparse representation would be good
    #build the sum of the 6 values in the neighborhood of the point (x,y,z)
    sum_nbh = lambda x,y,z,A: A[x+1,y,z] +A[x-1,y,z] +A[x,y+1,z] +A[x,y-1,z] + A[x,y,z+1] + A[x,y,z-1] 
    for id_x in range(grid_shape[0]):
        for id_y in range(grid_shape[1]):
            for id_z in range(grid_shape[2]):
                #check whether we hit a a voxel in the mesh
                if(voxels_np[id_x,id_y,id_z]==1):
                    sum_neighboring_values = sum_nbh(id_x,id_y,id_z, voxels_np)
                    #print('cds', id_x,id_y,id_z)
                    #print('sum neighbh', sum_neighboring_values)
                    if(sum_neighboring_values<6):
                        voxels_int[id_x,id_y,id_z] = 0
                        voxel_surface[id_x,id_y,id_z] = 1

    return voxels_int, voxel_surface

def voxel_carv_preprocess_numpy(voxels_np, thickness = 2):
    """
    Input: 
        voxels: An N x N x N numpy array that indicates the voxel indices of a filled mesh. 
                The values \in \{0,1\}
        thickness: the number of cubes, that should be the thickness of the boundary the voxel grid

    Output: 
        voxels_surface_np, voxels_interior_np . Two numpy arrays that have the same shape as voxels_np. The first one contains the voxels, that are in the surface, the second one contains the voxels, that are in the interior.
        In theory the sum of these two arrays should yield the input array again
    """
    boundary = np.zeros_like(voxels_np)
    interior, surface = voxel_surface_numpy(voxels_np)
    boundary +=surface
    for steps in range(thickness-1):
        interior, surface = voxel_surface_numpy(interior)
        boundary+=surface
    return interior, boundary


def center_of_mass(voxels_np):
    """
    Input: A numpy array (full) with the information whether the voxel is contained
    Output: The grid coordinates of the center of mass
    """
    grid_shape = voxels_np.shape
    counter = 0
    center = np.array([0.,0.,0.])
    for id_x in range(grid_shape[0]):
        for id_y in range(grid_shape[1]):
            for id_z in range(grid_shape[2]):
                #check whether we hit a a voxel in the mesh
                if(voxels_np[id_x,id_y,id_z]==1):
                    counter+=1
                    center = (1/float(counter))*np.array([float(id_x),float(id_y),float(id_z)]) + (float(counter-1)/float(counter))*center

    return([int(center[0]),int(center[1]),int(center[2])]) 
    

mesh_path = "./data/bunny_flipped_2.obj"
mesh = o3d.io.read_triangle_mesh(mesh_path)
output_voxel_filename = os.path.abspath("./data/bunny_flipped_2_voxelized.obj")
output_mesh_filename =os.path.abspath("./data/bunny_flipped_2_scaled.obj")
camera_path = os.path.abspath("./data/sphere.ply")
np_file = "./data/bunny_flipped_2_voxel"
json_filename = "./data/bunny_flipped_2_voxel.json"

visualization = True
cubic_size = 2.56 # 64 * 0.04
voxel_resolution = 128.0 #
mesh_scale = 20.0

mesh, voxel_grid, voxel_carving, voxel_surface = voxel_carving(mesh, output_voxel_filename, camera_path, cubic_size, voxel_resolution)

# We can directly zoom out mesh a little bit 
# to make sure that the voxel is inside
mesh.scale(mesh_scale, center=mesh.get_center())

o3d.io.write_voxel_grid(output_voxel_filename,voxel_grid)
o3d.io.write_triangle_mesh(output_mesh_filename, mesh)

#pdb.set_trace()

"""
print("surface mesh")
print(mesh)
o3d.visualization.draw_geometries([mesh])

print("surface voxels")
print(voxel_surface)
o3d.visualization.draw_geometries([voxel_surface])

print("carved voxels")
print(voxel_carving)
o3d.visualization.draw_geometries([voxel_carving])

print("combined voxels (carved + surface)")
print(voxel_grid)
o3d.visualization.draw_geometries([voxel_grid])
"""

#voxel = voxelizer(mesh_path, 10, 0.5, 2)
## the length of bounding box is 1/0.05=20

N_index = int(voxel_resolution)
voxel_matrix = np.zeros((N_index,N_index,N_index))

"""
for i in voxel_grid.get_voxels(): # index is from 1 to scale/size
    #print(i.grid_index)
    voxel_index = i.grid_index #a[0] a[1] a[2]
    voxel_matrix[voxel_index[0]-1,voxel_index[1]-1,voxel_index[2]-1] = 1
"""
voxel_matrix = voxel_to_numpy(voxel_grid, voxel_resolution = N_index)

print("The carving debugging: ")
inside, surface = voxel_carv_preprocess_numpy(voxel_matrix)
np.save(file="./data/bunny_flipped_2_voxel_surface",arr=np.array(surface, dtype=bool))
np.save(file="./data/bunny_flipped_2_voxel_int",arr=np.array(inside, dtype=bool))


print(" The center of mass is given by: ", center_of_mass(voxel_matrix))
voxel_write = { 
        "mesn_file" : output_mesh_filename,
        "voxel_origin" : (mesh_scale*(voxel_grid.origin)).tolist(), 
        "voxel_edge": cubic_size/voxel_resolution*mesh_scale,
        "voxel_matrix" : np.array(voxel_matrix, dtype=bool).tolist()
    } 
# voxel_edge is the edge length for each voxel


#with open(json_filename, "w", encoding='utf-8') as f:
#    json.dump(voxel_write, f, indent=4)

#np.save(file=np_file,arr=np.array(voxel_matrix, dtype=bool))



