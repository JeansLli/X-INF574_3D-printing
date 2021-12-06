import numpy as np
import matplotlib.pyplot as plt
import pdb


np.set_printoptions(threshold=np.inf)


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


def support_base(voxels_np):
    """
    Input: A numpy array (full) with the information whether the voxel is contained
    Output: the range of support bsae
    NOTE: The y axis is perpendicular to the support base. 
          The support base is close to y=0
    """
    grid_shape = voxels_np.shape
    
    for id_y in range(grid_shape[1]):
        if(np.count_nonzero(voxels_np[:,id_y,:]==True)>0):
            id_y+=1 #NOTE: After visualization, second floor is connected
            support_base = voxels_np[:,id_y,:]
            support_index = np.nonzero(support_base)
            #pdb.set_trace()
            max_x = np.max(support_index[0])
            min_x = np.min(support_index[0])
            max_z = np.max(support_index[1])
            min_z = np.min(support_index[1])
            center = np.array([int((max_x+min_x)/2), int((min_z+max_z)/2)])
            scaled_support_base = np.full((grid_shape[0],grid_shape[2]),False)
            scaled_support_base[center[0]-7:center[0]+7,center[1]-3:center[1]+3] = True
            if((np.logical_and(scaled_support_base,support_base)==scaled_support_base).all()):
                print("Support base is reasonable!!")
                return scaled_support_base

            ############ Visualization for support base!!!
            """
            visual = np.full((grid_shape[0],grid_shape[1],grid_shape[2]),False)
            visual_sb = np.full((grid_shape[0],grid_shape[1],grid_shape[2]),False)
            colors = np.empty(grid_shape, dtype=object)
            visual[:,id_y,:] = support_base
            visual_sb[:,id_y,:] = scaled_support_base
            colors[visual] = 'red'
            colors[visual_sb] = 'blue'
            ax = plt.figure().add_subplot(projection='3d')
            ax.voxels(visual,facecolors = colors, edgecolor='k')
            plt.show()
            #############
            """


def carving(voxel_surface,voxel_inside,support_base):

    grid_shape = voxel_surface.shape
    carved_voxel_inside = voxel_inside
    support_index = np.nonzero(support_base)
    max_x = np.max(support_index[0])
    min_x = np.min(support_index[0])
    max_z = np.max(support_index[1])
    min_z = np.min(support_index[1])
    com = center_of_mass(voxel_surface+voxel_inside) 
    com_x = com[0]
    com_z = com[2]
    if(com_x>=min_x and com_x<=max_x and com_z>=min_z and com_z<=max_z):
        return carved_voxel_inside
    # to move com_x, cut y-z plane
    # to move com_z, cut y-x plane
    
    if(com_x<min_x): #cut y-z plane
        #pdb.set_trace()
        for i in range(grid_shape[0]):
            
            if(carved_voxel_inside[i,:,:].any()==False):
                print("for x, skip ",i)
                continue
            else:
                cut_x = i
                break
               
        while(com_x<min_x and cut_x<grid_shape[0]):
            print("com_x=",com_x)
            print("min_x=",min_x)
            print("cut_x=",cut_x)
            print("com_z=",com_z)
            print("================")

            carved_voxel_inside[cut_x,:,:]=False
            cut_x+=1
            com = center_of_mass(voxel_surface+carved_voxel_inside) 
            com_x = com[0]
            com_z = com[2]

    if(com_x>max_x):
        cut_x = grid_shape[0]-1
        for i in range(grid_shape[0]):
            if(carved_voxel_inside[grid_shape[0]-i-1,:,:].any()==False):
                print("for x, skip ",grid_shape[0]-i-1)
                continue
            else:
                cut_x = grid_shape[0]-i-1
                break

        while(com_x>max_x and cut_x>=0):
            carved_voxel_inside[cut_x,:,:]=False
            cut_x+=1
            com = center_of_mass(voxel_surface+carved_voxel_inside) 
            com_x = com[0]
            com_z = com[2]
    

    if(com_z<min_z): #cut y-x plane
        for i in range(grid_shape[2]):
            if(carved_voxel_inside[:,:,i].any()==False):
                print("for z, skip ",i)
                continue
            else:
                cut_z = i
                break

        while(com_z<min_z and cut_z<grid_shape[0]):
            carved_voxel_inside[:,:,cut_z]=False
            cut_z+=1
            com = center_of_mass(voxel_surface+carved_voxel_inside) 
            com_x = com[0]
            com_z = com[2]

    if(com_z>max_z):
        for i in range(grid_shape[2]):
            if(carved_voxel_inside[grid_shape[2]-i-1,:,:].any()==False):
                print("for z, skip ",grid_shape[2]-i-1)
                continue
            else:
                cut_z = grid_shape[2]-i-1
                break
        
        while(com_z>max_z and cut_z>=0):
            carved_voxel_inside[:,:,cut_z]=False
            cut_z+=1
            com = center_of_mass(voxel_surface+carved_voxel_inside) 
            com_x = com[0]
            com_z = com[2]

    if (com_x >=min_x and com_x <=max_x and com_z >=min_z and com_z <=max_z):
        print("Carving is successful! The new center of mass is in the support base!")


    return carved_voxel_inside


voxel_surface = np.load('data/bunny_flipped_3_voxel_surface.npy')
voxel_inside = np.load('data/bunny_flipped_3_voxel_int.npy')


voxels = voxel_inside + voxel_surface
scaled_support_base = support_base(voxels)
carved_voxel_inside = carving(voxel_surface,voxel_inside,scaled_support_base)
np.save(file="./data/bunny_flipped_3_voxel_int_carved",arr=np.array(carved_voxel_inside, dtype=bool))




