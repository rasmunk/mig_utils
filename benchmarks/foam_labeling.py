# # Load libraries
# for image processing we use skimage, for saving results pandas

# In[1]:

import time
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from PIL import Image
from mig.io import IDMCShare


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
    share = IDMCShare('K2wzxDcEBm')
    img = imread('max_data/rec_8bit_ph03_cropC_kmeans_scale510.tif')
    #stack_image = share.read_binary('rec_8bit_ph03_cropC_kmeans_scale510.tif')
    #img = Image.frombytes(mode='L', size=(510, 510), data=stack_image)
    #img = np.array(img)
    #img = np.swapaxes(img, -1, -3)
    #img = np.swapaxes(img, -2, -3)

    load_stop = time.time()
    exe_start = time.time()
    foam_labelling(img)
    exe_stop = time.time()
    stop = time.time()

    load_time = str(load_stop - load_start)
    exe_time = str(exe_stop - exe_start)
    run_time = str(stop - start)
    img_size = str(sys.getsizeof(img) * pow(10, -6))

    with open("foam_times" + str(random.random())[10:], 'a') as fh:
        fh.write("load_time,exe_time,run_time,img_size\n")
        fh.write(",".join([load_time, exe_time, run_time, img_size]))

