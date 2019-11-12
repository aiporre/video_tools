#!/usr/bin/env python3

import sys
import argparse
from n2v.models import N2VConfig, N2V
from n2v.internals.N2V_DataGenerator import N2V_DataGenerator
import numpy as np
print('everything imported')

def generate_args(data_path, fileName = '*.png', dims = 'XY'):
    '''
    Generates the arguments to prepare data
    :param data_path: path to the training_images
    :return: dictionary of arguments
    '''
    args = {}
    args["baseDir"] = 'models'  # help="base directory in which your network will live"
    args["name"] = 'N2V'  # help="name of your network"
    args["dataPath"] = data_path  # help="The path to your training data"
    args["fileName"] = fileName  # help="name of your training data file"
    args["validationFraction"] = 5.0  # help="Fraction of data you want to use for validation (percent)"
    args["dims"] = dims  # help="dimensions of your data, can include: X,Y,Z,C (channel), T (time)"
    args["patchSizeXY"] = 64  # help="XY-size of your training patches"
    args["patchSizeZ"] = 64  # , help="Z-size of your training patches"
    args["epochs"] = 100  #  help="number of training epochs"
    args["stepsPerEpoch"] = 400  # help="number training steps per epoch"
    args["batchSize"] = 64  # help="size of your training batches"
    args["netDepth"] = 2  # help="depth of your U-Net"
    args["netKernelSize"] = 3  # help="Size of conv. kernels in first layer"
    args["n2vPercPix"] = 1.6  # help="percentage of pixels to manipulated by N2V"
    args["learningRate"] = 0.0004  # help="initial learning rate"
    args["unet_n_first"] = 32  # help="number of feature channels in the first u-net layer"

    return argparse.Namespace(**args)

def prepare_training_data(args):
    '''

    :param args:
    :return: model, training samples X , validation samples X_val
    '''

    datagen = N2V_DataGenerator()
    dim = args.dim
    try:
        imgs = datagen.load_imgs_from_directory(directory=args.dataPath, dims=args.dims, filter=args.fileName)
    except Exception as e:
        if args.dim == 'XY':
            dim = 'YXC'
        elif args.dim == 'YX':
            dim = 'YXC'
        elif args.dim == 'YXC':
            dim = 'XY'
        elif args.dim == 'XYC':
            dim = 'XY'
        else:
            raise Exception('Bad dimension input: ' + str(dim) + '.')
        print('WARINING: ERROR loading. Attemting to load with other dimension. Last ', args.dim,'. Current ', dim)
        imgs = datagen.load_imgs_from_directory(directory=args.dataPath, dims=args.dims, filter=args.fileName)
    print('Making as as float 32')
    imgs = [img.astype(np.float32) for img in imgs]
    print("number of images to train: ", len(imgs))
    print("imgs.shape", imgs[0].shape)
    if 'C' in dim and imgs[0].shape[-1]==4:
        print('prev shape of images: ', imgs.shape)
        imgs = np.array([im[...,0:2] for im in imgs])
        print('new shape of images: ', imgs.shape)

    # Here we extract patches for training and validation.
    pshape = (args.patchSizeXY, args.patchSizeXY)
    if 'Z' in args.dims:
        pshape = (args.patchSizeZ, args.patchSizeXY, args.patchSizeXY)

    print(pshape)
    patches = datagen.generate_patches_from_list(imgs[:1], shape=pshape)
    print(patches.shape)

    # The patches are non-overlapping, so we can split them into train and validation data.
    frac = int((len(patches))*float(args.validationFraction)/100.0)
    print("total no. of patches: "+str(len(patches))+"\ttraining patches: "+str(
        len(patches)-frac)+"\tvalidation patches: "+str(frac))
    X = patches[frac:]
    X_val = patches[:frac]

    config = N2VConfig(X, unet_kern_size=args.netKernelSize,
                       train_steps_per_epoch=int(args.stepsPerEpoch), train_epochs=int(args.epochs), train_loss='mse',
                       batch_norm=True,
                       train_batch_size=args.batchSize, n2v_perc_pix=args.n2vPercPix, n2v_patch_shape=pshape,
                       n2v_manipulator='uniform_withCP', n2v_neighborhood_radius=5,
                       train_learning_rate=args.learningRate,
                       unet_n_depth=args.netDepth,
                       unet_n_first=args.unet_n_first
                       )

    # Let's look at the parameters stored in the config-object.
    vars(config)

    # a name used to identify the model
    model_name = args.name
    # the base directory in which our model will live
    basedir = args.baseDir
    # We are now creating our network model.
    model = N2V(config=config, name=model_name, basedir=basedir)

    return model, X, X_val

def train_model(model, X, X_val):
    '''

    :param model: model to train
    :param X: training samples
    :param X_val: validation samples
    :return: history dictionary from tensorflow
    '''
    return model.train(X,X_val)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--baseDir", help="base directory in which your network will live", default='models')
    parser.add_argument("--name", help="name of your network", default='N2V')
    parser.add_argument("--dataPath", help="The path to your training data")
    parser.add_argument("--fileName", help="name of your training data file", default="*.tif")
    parser.add_argument("--validationFraction", help="Fraction of data you want to use for validation (percent)",
                        default=5.0, type=float)
    parser.add_argument("--dims", help="dimensions of your data, can include: X,Y,Z,C (channel), T (time)",
                        default='YX')
    parser.add_argument("--patchSizeXY", help="XY-size of your training patches", default=64, type=int)
    parser.add_argument("--patchSizeZ", help="Z-size of your training patches", default=64, type=int)
    parser.add_argument("--epochs", help="number of training epochs", default=100, type=int)
    parser.add_argument("--stepsPerEpoch", help="number training steps per epoch", default=400, type=int)
    parser.add_argument("--batchSize", help="size of your training batches", default=64, type=int)
    parser.add_argument("--netDepth", help="depth of your U-Net", default=2, type=int)
    parser.add_argument("--netKernelSize", help="Size of conv. kernels in first layer", default=3, type=int)
    parser.add_argument("--n2vPercPix", help="percentage of pixels to manipulated by N2V", default=1.6, type=float)
    parser.add_argument("--learningRate", help="initial learning rate", default=0.0004, type=float)
    parser.add_argument("--unet_n_first", help="number of feature channels in the first u-net layer", default=32,
                        type=int)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    print(args)
    print("args", str(args.name))

    print('------------------------------------')
    print('------ DATA PREPARATION ---')
    print('------------------------------------')
    model, X, X_val = prepare_training_data(args)
    print('------------------------------------')
    print("------ BEGIN TRAINING -----")
    print('------------------------------------')
    history = model.train(X, X_val)

