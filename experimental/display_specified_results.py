"""Ipython kernel for displaying select images"""
import os
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib
import SimpleITK as sitk

from autil import get_data_paths, get_new_images
import constants
from database import db_img_predict

# Pathway 1 use data from DATABASE with specific criteria:
db_nan = db_img_predict()
db_nan()
df = db_nan.df

df = df[df['logo_class'].isna()]
lst_img_id = df['img_id'].tolist()
random.shuffle(lst_img_id)
lst_rand_dat = lst_img_id[:15]

lst_images_urls = None  # generated with identifying information removed

# Pathway 2 just specify URLs directly in a list:
# lst_images_urls = None  # generated with identifying information removed

get_new_images(lst_images_urls)
for img_url in lst_images_urls:
    fname_img = os.path.basename(img_url)
    fpath_img = os.path.join(constants.DATA_PATH, fname_img)
    img_array = sitk.ReadImage(fpath_img)
    nda = sitk.GetArrayViewFromImage(img_array)
    ysize = nda.shape[0]
    xsize = nda.shape[1]
    margin = 3
    dpi = 120
    figsize = (1 + margin) * ysize / dpi, (1 + margin) * xsize / dpi
    img = mpimg.imread(fpath_img)
    plt.figure(figsize=figsize, dpi=dpi)  #if using in jupyter kernerl this
    #  enlarges the size
    plt.figure()
    plt.axis('off')
    plt.imshow(img)
    plt.show(block=True)
