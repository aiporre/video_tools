from n2v.models import N2V
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imread, imsave
from csbdeep.io import save_tiff_imagej_compatible

class N2VDenoiser(object):
    def __init__(self):
        model_name = 'n2v_2D'
        basedir = 'models'
        self.model = N2V(config=None, name=model_name, basedir=basedir)
    def __call__(self):
	return  model.predict(img, axes='YXC')
        
