# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage.morphology import convex_hull_image as chull
from skimage.io import imread, imsave
from scipy import ndimage as ndi
from scipy.ndimage.morphology import distance_transform_edt as distmap
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from skimage.measure import regionprops

# In[2]:


# Create random test image
Z = np.random.random((50, 50, 3))
imsave(fname='test_image.tiff', arr=Z, plugin='pil')
stack_image = imread('test_image.tiff')
print(stack_image.shape, stack_image.dtype)

# In[ ]:

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
for i, (cax, clabel) in enumerate(zip([ax1, ax2, ax3], ['xy', 'zy', 'zx'])):
    cax.imshow(np.sum(stack_image, i).squeeze(), interpolation='none',
               cmap='bone_r')
    cax.set_title('%s Projection' % clabel)
    cax.set_xlabel(clabel[0])
    cax.set_ylabel(clabel[1])

# In[ ]:


plt.imshow(stack_image[0], cmap='bone')

# In[ ]:


bubble_image = np.stack([chull(csl > 0) & (csl == 0) for csl in stack_image])
plt.imshow(bubble_image[5] > 0, cmap='bone')

# In[ ]:


bubble_invert = np.invert(bubble_image)
plt.imshow(bubble_invert[15], cmap='bone')

# In[ ]:


bubble_dist = distmap(bubble_invert)
plt.imshow(bubble_dist[25, :, :], interpolation='none', cmap='jet')

# In[ ]:


bubble_candidates = peak_local_max(bubble_dist, min_distance=12)
print('Found', len(bubble_candidates), 'bubbles')
df = pd.DataFrame(data=bubble_candidates, columns=['x', 'y', 'z'])
df.to_csv('bubble.candidates.csv')
bubble_seeds = peak_local_max(bubble_dist, min_distance=12, indices='false')
plt.imshow(np.sum(bubble_seeds, 0).squeeze(), interpolation='none',
           cmap='bone_r')

# In[ ]:


markers = ndi.label(bubble_seeds)[0]
cropped_markers = markers[0:30, 0:30, 0:30]
cropped_bubble_dist = bubble_dist[0:30, 0:30, 0:30]
cropped_bubble_inver = bubble_invert[0:30, 0:30, 0:30]
labeled_bubbles = watershed(-cropped_bubble_dist, cropped_markers,
                            mask=cropped_bubble_inver)
# plt.imshow(labeled_bubbles[10,:,:], cmap=plt.cm.spectral,
#            interpolation='nearest')


# In[ ]:


props = regionprops(labeled_bubbles)
