# # Load libraries
# for image processing we use skimage, for saving results pandas

# In[1]:

import time
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from mig.io.image_plugins import imread
from mig.io import IDMCShare, ERDAShare, SFTPStore, SSHFSStore


def foam_labelling(stack_image):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
        cax.imshow(np.sum(stack_image, i).squeeze(), interpolation='none', cmap='bone_r')
        cax.set_title('%s Projection' % clabel)
        cax.set_xlabel(clabel[0])
        cax.set_ylabel(clabel[1])

    from skimage.morphology import convex_hull_image as chull
    bubble_image = np.stack([chull(csl > 0) & (csl == 0) for csl in stack_image])
    bubble_invert = np.invert(bubble_image)

    from scipy import ndimage as ndi
    from scipy.ndimage.morphology import distance_transform_edt as distmap
    bubble_dist = distmap(bubble_invert)

    # # Watershed segmentation
    from skimage.feature import peak_local_max
    from skimage.morphology import watershed
    bubble_seeds = peak_local_max(bubble_dist, min_distance=12, indices='false')

    markers = ndi.label(bubble_seeds)[0]
    cropped_markers = markers[50:450, 50:450, 50:450]
    cropped_bubble_dist = bubble_dist[50:450, 50:450, 50:450]
    cropped_bubble_inver = bubble_invert[50:450, 50:450, 50:450]
    labeled_bubbles = watershed(-cropped_bubble_dist, cropped_markers,
                                mask=cropped_bubble_inver)

    # interpolation='nearest')
    # Feature properties
    from skimage.measure import regionprops
    props = regionprops(labeled_bubbles)
    props[200].filled_area

# # Read in data
# in this case a 3D tif stack of tomographic slices

# %%time
# stack_image = IDMCShare('K2wzxDcEBm').read_binary(
# 'rec_8bit_ph03_cropC_kmeans_scale510.tif')
# print(type(stack_image))
# stack_image = np.swapaxes(stack_image, -1, -3)
# stack_image = np.swapaxes(stack_image, -2, -3)
# with open('max_data/rec_8bit_ph03_cropC_kmeans_scale510.tif', 'wb') as fh:
#    fh.write(stack_image)


if __name__ == "__main__":
    start = time.time()
    load_start = time.time()
    share = SFTPStore("io.idmc.dk", username='K2wzxDcEBm', password='K2wzxDcEBm')
    file = 'rec_8bit_ph03_cropC_kmeans_scale510.tif'
    with share.open(file, 'r') as fh:
        v = imread(fh)
        plt.imshow(v[100], cmap='bone')
        # foam_labelling(v)