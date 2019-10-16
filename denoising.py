try:
    from n2v.models import N2V
except Exception as e:
    print('Importing exception noise to void: ', e)
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imread, imsave
from csbdeep.io import save_tiff_imagej_compatible
from skimage import exposure



class N2VDenoiser(object):
    def __init__(self):
        model_name = 'n2v_2D'
        basedir = 'models'
        try:
            self.model = N2V(config=None, name=model_name, basedir=basedir)
        except Exception as e:
            print('Exception: ', e)
    def __call__(self):
        return  model.predict(img, axes='YXC')

class ContrastDenoiser(object):
    def __call__(self,img):
        img_eq = exposure.equalize_hist(img)
        return img_eq
