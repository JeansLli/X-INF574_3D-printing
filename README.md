# X-INF574_3D-printing

1. Read the mesh.Specify desired center of mass, support base and graviry direction.
2. Compute the target center of mass.
3. Build the voxlization and boolean for the voxels (inside and outside).
4. Compute the current center of mass.
5. Look at the deviation from the target center of mass.
6. Start carving at the "right" side of the mesh.("right" means the side where the current center of mass lie.)
7. Compute the current center of mass and stop if the center of mass is in the vertical rigion of support base.
8. Deforming.
9. Repeat from step 4 and step 8 until convergence.


##Voxelization of the 3d model##

Give your 3d shape some name and specify the path of your .obj in the voxelizer.py file. You can adapt the number of voxels with the variable voxel_resolution in the voxelizer.py file. Note that a large number of voxels slow down the computation a lot.

##Support Base for the carved model##
If the voxelization was successful you have by now in the data folder a saved numpy array of size voxel_resolution x voxel_resolution x voxel_resolution. Next you need to run the carving.py file. You do not need to worry about the name and paths of the models and numpy arrays. Just give the variable "name" the same value as in voxelizer.py.

Note that you can change the size of the support base. In carving.py in line 51 you can change the line 

```python
scaled_support_base[center[0]-1:center[0]+1,center[1]:center[1]+1] = True
```

You can change the parameters to change the size in x and z direction of your support base.

If the support base is reasonable, i.e if it is contained entirely in the base, the carving process will start. For that we will detact on which side we have "too much mass". We will then try to carve this mass away such that the center of mass is in the area of the support base.

If this works, you can run the numpy_to_stl.py file. Note that you need to change the path of your input numpy array to 
"data/"<name>+"_voxel_entire_carved.npy". Then specify the output name and don't forget the .stl ending.

If the Carving fails, you need to change the shape of your mesh. To do this, you can load your original .obj file into the houdini program "\cage_based_deformation.hipnc" and then you can try to modify the shape of your surface such that it is more benefitial for the carving. Then try to repeat this pipeline again with the deformed shape.




