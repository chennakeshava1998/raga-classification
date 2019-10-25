import imageio
import glob, os
import numpy as np
import matplotlib.pyplot as plt
import visvis

import config

def get_img_data(raga):
    """ 
    Returns the images of all the fft's of a raga
    Args:
    raga: config.IMG_<raga_name>

    Returns:
    nd array of features
    """
    filelist=glob.glob(os.path.join(raga, "*.png"))
    features = []

    for filename in filelist:
        im = imageio.imread(filename)
        features.append(im)
        #visvis.imshow(im)
	
    return features

def test_get_img_data():
    begada_fft = get_img_data(config.IMG_BEGADA)

    for i in range(len(begada_fft)):
        print(begada_fft[i].shape)

#get_img_data("../img_data/begada")
