import open3d as o3d
import numpy as np
import pdb
import json

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


def voxel_inside(voxel_grid, voxel):
    """ 
    Input: A voxel grid and one voxel with x,y,z coordinates in the grid. 
    Output: boolean whether the voxel is inside or outside.
    We will shoot a ray in all 6 directions starting from the voxel. If each ray hits a voxel in the boundary, we say that the point is inside.
    Note that this is a limitation. For fine meshes, where we have a "blister", that turns to the inside, this algorithm can fail.
    """
    pass

def voxelizer(mesh_path, scale, size, gap):
    """
    scale: the scale of bounding box of mesh
    size: the size of cubic<y
    """
    mesh = read_mesh(mesh_path)
    mesh.scale(scale / np.max(mesh.get_max_bound() - mesh.get_min_bound()),center=mesh.get_center())
    voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh,voxel_size=size)
    N_axis = int(scale / size)
    #N_axis is the number of voxels we want to have per axis.
    #The voxel_matrix is a N_axis x N_axis x N_axis matrix, i.e a 3-D grid. The value of each gridpoint will indicate whether the point is included  
    voxel_matrix = np.zeros((N_axis,N_axis,N_axis))
    #matrix that will store all the voxels, that are mot in the boundary. This will be the one, which we will carve
    inner_voxels = np.zeros((N_axis,N_axis,N_axis))
    #pdb.set_trace()
    center_point = voxel_grid.get_center() # the geometric coordinates
    center_index = voxel_grid.get_voxel(center_point) 
    print("center point",center_point)
    print("center_index",center_index)
    
    for i in voxel_grid.get_voxels(): # index is from 1 to scale/size
        #print(i.grid_index)
        a = i.grid_index #a[0] a[1] a[2]
        voxel_matrix[a[0]-1,a[1]-1,a[2]-1] = 1
    print("before fill=",voxel_matrix.sum())
    before_voxel = voxel_matrix

    # to fill the inside voxel 
    for i in range(N_axis):
        for j in range(N_axis): 
            start = 0
            end = N_axis-1 
            for k in range(N_axis):
                if(voxel_matrix[i,j,k]==1):
                    start = k
                    break;
            for k in range(N_axis):
                if(voxel_matrix[i,j,N_axis-k-1]==1):
                    end = N_axis-k-1
                    break
            for k in range(start, end+1):
                if(k<(start+gap) or k>(end-gap)):
                    voxel_matrix[i,j,k] = 0
                    #print("gap",k)
                else:
                    voxel_matrix[i,j,k] = 1
            #print("------------")

            #if(start ==0 and end==N_axis-1):
            #    print("warning",i,j)
    print("after fill = ", voxel_matrix.sum())
    o3d.visualization.draw_geometries([voxel_grid])

    #find one voxel inside the mesh
    #take a voxel on the surface. Then one of the 6 neigbours will be in the inside of the mesh. Check this by shooting from that point a ray in all 6 directions.
    #then start a bfs from this inner voxel to determine all inner voxel points.
    
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

voxel = voxelizer(mesh_path, 10, 0.5, 2)
## the length of bounding box is 1/0.05=20


file_name = "./data/voxel_new.json"

with open(file_name, "w", encoding='utf-8') as f:
    #json.dump(voxel_matrix.tolist(),f,separators=(',', ':'))
    json.dump(voxel, f, indent=4)
