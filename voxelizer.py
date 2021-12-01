import open3d as o3d
import numpy as np

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


def voxelizer(mesh, size ):
    mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()),center=mesh.get_center())
    voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh,voxel_size=0.05)
    print(voxel_grid.VoxelGrid)
    #o3d.visualization.draw_geometries([voxel_grid])


bunny = read_mesh("./data/bunny.obj")
voxelizer(bunny,0)