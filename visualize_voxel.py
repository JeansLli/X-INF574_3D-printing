import numpy as np
import matplotlib.pyplot as plt

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

name= 'rocket_flipped'
#name = "bunny_flipped_3"

#input array to visualize
voxel_surface = np.load('data/'+name+'_voxel_surface.npy')
voxel_inside = np.load('data/'+name+'_voxel_int.npy')

voxels = voxel_inside + voxel_surface

com = center_of_mass(voxels)

print('voxels', voxels.shape)

print('voxel occ', np.count_nonzero(voxels==True))


voxels[:,:,:com[2]] = np.full((256,256,com[2]),False)
# prepare some coordinates

#print('mass total', np.count_nonzero(voxels==True))
print('mass interior', np.count_nonzero(voxel_inside==True))
# draw cuboids in the top left and bottom right corners, and a link between
# them
ctr = np.full((256,256,256),False)
ctr[com[0],com[1],com[2]]=True


# combine the objects into a single boolean array

# set the colors of each object
colors = np.empty(voxels.shape, dtype=object)
colors[voxel_surface] = 'red'
colors[voxel_inside] = 'blue'

colors[ctr] = 'yellow'
#colors[cube2] = 'green'
# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(voxels,facecolors = colors, edgecolor='k')
plt.show()
