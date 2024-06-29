import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_patch(ax, cx, cy, dx, dy):
    """ Helper function to create and add a rectangle patch to the plot. """
    rect = patches.Rectangle((cx - dx / 2, cy - dy / 2), dx, dy, linewidth=1, edgecolor='black', facecolor='black')
    ax.add_patch(rect)


def check_and_adjust_patch(patchCoords, current_patch, threshold):
    """ Check and adjust the current patch to maintain the threshold distance from others. """

    gridLength = 6
    gridWidth = 3

    

    cx, cy, dx, dy, offX, offY = current_patch
    
    idx = len(patchCoords)

    if idx ==0:
      return [cx, cy, dx, dy, offX, offY]


    # parameters of left patch
    if len(patchCoords) > 0:
      cx_left , cy_left , dx_left, dy_left, _, _ = patchCoords[idx-1]
      # check for left patch
      if 0 <= cx-dx/2 - (cx_left + dx_left/2) <= threshold:
        dx += threshold*1.2
        cx -= threshold*1.2/2


    # parameters of below patch
    if len(patchCoords) >= gridWidth:
      cx_b , cy_b, dx_b, dy_b, _, _ = patchCoords[idx-gridWidth] 
      # check for bottom patch 
      if 0 <= cy - dy/2 - (cy_b + dy_b/2) <= threshold:
         dy += threshold * 1.2
         cy -= threshold *1.2/2

    # parameter of patch right to below patch
    if len(patchCoords) >= gridWidth -1:
      cx_rightb, cy_rightb, dx_rightb, dy_rightb, _, _ = patchCoords[idx-gridWidth+1] 
      # check for right bottom patch
      # check if it is below or in level of current patch
      if cy - dy/2 >= cy_rightb + dy_rightb/2:
        # check if it is in the level or to right of current patch
        if cx + dx/2 > cx_rightb - dx_rightb/2:
          # check if vertical distance between them is less than threshold
          if 0 <= cy-dy/2 - (cy_rightb + dy_rightb/2) <= threshold:
            dy += threshold * 1.2
            cy -= threshold*1.2/2
            if 0 <= cy - dy/2 - (cy_b + dy_b/2) <= threshold:
              dy+= threshold *1.2
              cy-= threshold*1.2/2

      if cy - dy/2 < cy_rightb + dy_rightb/2:
        # check horizontal distance between them
        if 0 <= cx_rightb - dx_rightb/2 - (cx + dx/2) <= threshold:
          dx += threshold *1.2
          cx += threshold * 1.2/2        

      

    
    # parameters of patch below the left patch
    if len(patchCoords) >= gridWidth + 1:
      cx_leftb, cy_leftb , dx_leftb, dy_leftb, _, _ = patchCoords[idx-gridWidth-1]
      # check for left bottom patch
      if cy - dy/2 >= cy_leftb + dy_leftb/2:
        # check if it is in the level or to left of current patch
        if cx_leftb + dx_leftb/2 > cx - dx/2:
          # check if vertical distance between them is less than threshold
          if 0 <= cy-dy/2 - (cy_leftb + dy_leftb/2) <= threshold:
            dy += threshold *1.2
            cy -= threshold *1.2/2
            if cy_b + dy_b/2 >= cy_rightb + dy_rightb/2:
              if 0 <= cy - dy/2 - (cy_b + dy_b/2) <= threshold:
                dy += threshold *1.2
                cy -= threshold *1.2/2
                if 0 <= cy - dy/2 - (cy_rightb + dy_rightb/2) <= threshold:
                  dy += threshold *1.2
                  cy -= threshold *1.2/2
            if cy_b + dy_b < cy_rightb + dy_rightb/2:
              if 0 <= cy - dy/2 - (cy_rightb + dy_rightb/2) <= threshold:
                dy += threshold *1.2
                cy -= threshold*1.2/2
                if 0 <= cy - dy/2 - (cy_b + dy_b/2) <= threshold:
                  dy += threshold *1.2
                  cy -= threshold *1.2/2



      if cy - dy/2 < cy_leftb + dy_leftb/2: 
        # check horizontal distance between them
        if 0 <= cx - dx/2 - (cx_leftb + dx_leftb/2) <= threshold:
          dx += threshold *1.2      
          cx -= threshold *1.2/2 
          if 0 <= cx - dx/2 - (cx_left + dx_left/2)  <= threshold:
            dx += threshold *1.2
            cx -= threshold *1.2/2

      if cy - dy/2 < cy_rightb + dy_rightb/2:
        # check horizontal distance between them
        if 0 <= cx_rightb - dx_rightb/2 - (cx + dx/2) <= threshold:
          dx += threshold *1.2
          cx += threshold *1.2/2         

    return [cx, cy, dx, dy, offX, offY]



def simulate_designs(n=5 , gridSize=6, pxSize=0.00575, threshold=0.5e-3, inclusion_ratio=0.8):

    # Board boundaries
    minX = -(gridSize / 2) * pxSize
    maxX = (gridSize / 2) * pxSize
    minY = -(gridSize / 2) * pxSize
    maxY = (gridSize / 2) * pxSize

    # Feed location
    yc = 0  # Y center for the feed
    xc = -(gridSize / 2) * pxSize + pxSize / 2  # X center for the feed
    xDel = 1 * pxSize  # X delta for the feed
    yDel = 2 * pxSize  # Y delta for the feed

    all_patch_coords = []  # List to hold coordinates for all designs
    all_designs = []
    
    halfGridSize = 3

    # Main loop for generating designs
    for i in range(n):
        patchCoords = []  # Initialize array for patch storage
       
        grid = {}  # Dictionary to hold patches by their grid positions

        # Loop to create patches
        for j in range(gridSize):
            for k in range(halfGridSize):

                if j==0:
                  if k == halfGridSize-1:
                     dx = pxSize * 1.5 # to ensure total metal for feed
                     dy = pxSize 
                  else:
                     dx = pxSize
                     dy = pxSize   
                  offX = 0
                  offY = 0
                  cx = (k + 0.5) * pxSize + offX - (gridSize / 2) * pxSize
                  cy = (j + 0.5) * pxSize + offY - (gridSize / 2) * pxSize 
                  current_patch = [cx, cy, dx, dy, offX, offY]
                  

                else:
                  # Choose length and width randomly in a particular range
                  dx = pxSize * (0.85 + 0.35 * np.random.rand()) 
                  dy = pxSize * (0.85 + 0.35 * np.random.rand())

                  # Choose offset of center from the grid-point (k, j)
                  offX = pxSize * (0.05 + (0.2 - 0.05) * np.random.rand()) * np.random.choice([-1, 1])
                  offY = pxSize * (0.05 + (0.2 - 0.05) * np.random.rand()) * np.random.choice([-1, 1])



                  # Set the coordinates of center according to the offset
                  cx = (k + 0.5) * pxSize + offX - (gridSize / 2) * pxSize
                  cy = (j + 0.5) * pxSize + offY - (gridSize / 2) * pxSize

                  # Ensure that all patches are within the board boundary
                  cx = max(minX + dx / 2, min(maxX - dx / 2, cx))
                  cy = max(minY + dy / 2, min(maxY - dy / 2, cy))

                  if k == halfGridSize:
                    if 0 <= 0 - (cx + dx/2) <= threshold:
                      dx += threshold * 1.2
                      cx += threshold * 1.2 /2


                

                # Store the current patch temporarily
                current_patch = [cx, cy, dx, dy, offX, offY]

                # Check and adjust with existing patches
                
                if len(patchCoords) > 0:
                    current_patch = check_and_adjust_patch(patchCoords, current_patch, threshold)
                # Store parameters of the patch after adjustment
                patchCoords.append(current_patch)

        
        num_patches_left = (gridSize - 1) * halfGridSize  # Calculate number of patches in the left half
        inclusion_array = np.random.choice([0, 1], num_patches_left, p=[1-inclusion_ratio, inclusion_ratio])

        # Apply the inclusion array to patchCoords
        for idx, included in enumerate(inclusion_array):
            if included == 0:
                patchCoords[idx + halfGridSize] = [0, 0, 0, 0, 0, 0]  # Set to zero if not included
        

        # Mirror the design to the right half
        mirrored_patches = []
        for patch in patchCoords:
            cx, cy, dx, dy, offX, offY = patch
            mirror_cx = -cx  # Mirroring the x-coordinate
            mirrored_patch = [mirror_cx, cy, dx, dy, -offX, offY]
            mirrored_patches.append(mirrored_patch)

        patchCoords.extend(mirrored_patches)  # Add mirrored patches to the main list
        

        all_patch_coords.extend(patchCoords)

        # Plotting the design
        # fig, ax = plt.subplots(figsize=(8, 6))  # Adjusting the figsize to zoom in
        # ax.set_xlim(minX, maxX)
        # ax.set_ylim(minY, maxY)
        # for coord in patchCoords:
        #     create_patch(ax, *coord[:4])
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.show()



    # Convert all_patch_coords to a numpy array for easier handling
    all_patch_coords_array = np.array(all_patch_coords)

    # Save all coordinates to a file
    np.savetxt('/Users/at/Documents/patchcoords.txt', all_patch_coords_array, delimiter=',', fmt='%f')
    print('All patch coordinates saved to patchcoords.txt')



simulate_designs()

