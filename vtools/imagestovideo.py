import os

import cv2
import argparse
from .denoising import ContrastDenoiser, N2VDenoiser
from .pipeline import PipeLine
from tqdm import tqdm

class ImageToVideo(object):
    '''
    Creates a video
    '''
    def __init__(self, split=-1, transform=None, gray='y'):
        # Create a VideoCapture object
        self.split = split
        self.transform = transform
        if gray == 'y':
            self.isColor = False
        else:
            self.isColor = True

    def set_output(self, frame_width, frame_height, output_path = 'output.avi',fps=30):
        self.output_path = output_path
        self.frame_counter = 0
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(frame_width)
        self.frame_height = int(frame_height)

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
        if self.split>0:
            output_path = self.output_path[:-4]+"_1.avi"
            self.part_counter = 1

        self.output_video = cv2.VideoWriter(output_path, self.codec, fps, (self.frame_width, self.frame_height), isColor=self.isColor)

    def new_output(self):
        self.output_video.release()
        self.part_counter += 1
        new_output_path = self.output_path[:-4]+ "_" + str(self.part_counter) + ".avi"
        self.output_video = cv2.VideoWriter(new_output_path, self.codec, 30, (self.frame_width, self.frame_height), isColor=self.isColor)

    def update(self, frame):
        # Increase the counter for automatic split of the next frame
        self.frame_counter +=1
        # Verify if split is necesary
        K = (1800*self.split)
        # transform the frame if necesary
        if self.transform is not None:
            self.frame_tr = self.transform(frame)
            self.frame_tr = (255.0*self.frame_tr).astype('uint8')
        else:
            self.frame_tr  = frame
        if self.split>0 and self.frame_counter % K == 0:
            self.new_output()

        # Save  frame into video output file
        self.output_video.write(self.frame_tr)

    def close(self):
        self.output_video.release()


class ToGray(object):
    '''
    Tranformation function class convert image to grayscale
    '''
    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
