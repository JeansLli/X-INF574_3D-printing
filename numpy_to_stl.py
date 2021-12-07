from voxelfuse.voxel_model import VoxelModel
from voxelfuse.mesh import Mesh
from voxelfuse.primitives import generateMaterials
import numpy as np

if __name__ == '__main__':

    voxel_numpy = np.load('data/bunny_flipped_3_voxel_entire_carved.npy')
    model = VoxelModel(voxel_numpy, generateMaterials(4))
    mesh = Mesh.fromVoxelModel(model)
    mesh.export('bunny_3_flipped_carved.stl')
    