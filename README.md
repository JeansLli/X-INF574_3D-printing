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


Note that for compilation libigl is required. It can be downloaded from source here: https://github.com/libigl/libigl
Note that with our cmake, the location of the folder is not important.

