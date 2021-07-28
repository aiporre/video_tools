try:
    from n2v.models import N2V
except Exception as e:
    print('Importing exception noise to void: ', e)
import numpy as np
from skimage import exposure

def normalize(img):
    if len(img.shape) == 2:
        img = (img-img.min())/(img.max()-img.min())
    elif len(img.shape) == 3:
        for i in range(3):
            img[...,i] = (img[...,i]-img[...,i].min())/(img[...,i].max()-img[...,i].min())
    else:
        raise Exception('image must be YX or YXC. Shape found Found '+ str(img.shape))
    return img

class N2VDenoiser(object):
    def __init__(self):
        model_name = 'N2V'
        basedir = 'models'
        try:
            self.model = N2V(config=None, name=model_name, basedir=basedir)
        except Exception as e:
            print('Exception: ', e)
        axes = self.model.config.axes
        assert axes in ['YX','YXC'], 'Not supported axes configuration ' + str(axes) + '. Supported options are ' + str(['YX','YXC'])
        self.axes = axes

    def __call__(self,img):
        if img.max()>1.0 or img.min()<0.0:
            img = normalize(img)
        if len(img.shape) == 2:
            axes = 'YX'
        elif len(img.shape) == 3:
            axes = 'YXC'
        else:
            raise Exception('Invalid format image: ', img.shape, 'formats supported YX and YXC')
        pred = self.model.predict(img, axes=axes)
        pred = np.clip(pred,0.0,1.0)
        return pred
class ContrastDenoiser(object):
    def __call__(self,img):
        img_eq = exposure.equalize_hist(img)
        return img_eq
