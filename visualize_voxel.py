import numpy as np
import matplotlib.pyplot as plt


#input array to visualize
voxel_surface = np.load('data/bunny_flipped_2_voxel_surface.npy')
voxel_inside = np.load('data/bunny_flipped_2_voxel_int.npy')

voxels = voxel_inside+voxel_surface
print('voxels', voxels.shape)

print('voxel occ', np.count_nonzero(voxels==True))

#voxels[:,:40,:] = np.full((128,40,128),False)
voxels[:,:,:67] = np.full((128,128,67),False)
# prepare some coordinates

#print('mass total', np.count_nonzero(voxels==True))
print('mass interior', np.count_nonzero(voxel_inside==True))
# draw cuboids in the top left and bottom right corners, and a link between
# them
ctr = np.full((128,128,128),False)
ctr[62,54,67]=True


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
