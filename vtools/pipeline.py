class PipeLine(object):
    def __init__(self, transforms):
        assert isinstance(transforms, list), 'tranforms have to be a list'
        self.transforms = transforms

    def __call__(self, img):
        for t in self.transforms:
            img = t(img)
        return img
