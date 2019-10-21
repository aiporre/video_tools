import os

import cv2
import argparse
from .denoising import ContrastDenoiser, N2VDenoiser
from .pipeline import PipeLine
from tqdm import tqdm

class VideoToVideo(object):
    def __init__(self, src=0, output_path = 'output.avi', split=-1, transform=None):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        self.output_path = output_path
        self.split = split
        self.frame_counter = 0
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
        if self.split>0:
            output_path = self.output_path[:-4]+"_1.avi"
            self.part_counter = 1
        self.output_video = cv2.VideoWriter(output_path, self.codec, 30, (self.frame_width, self.frame_height), isColor=False)
        
        #transform object is applied to each image frame
        self.transform = transform

    def new_output(self):
        self.output_video.release()
        self.part_counter += 1
        new_output_path = self.output_path[:-4]+ "_" + str(self.part_counter) + ".avi"
        self.output_video = cv2.VideoWriter(new_output_path, self.codec, 30, (self.frame_width, self.frame_height), isColor=False)

    def update(self):
        # Read the next frame 
        if self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            self.frame_counter +=1
        # Verify if split is necesary
        K = (1800*self.split)
        if self.status:
            if self.transform is not None:
                self.frame_tr = self.transform(self.frame)
                self.frame_tr = (255.0*self.frame_tr).astype('uint8')
        if self.split>0 and self.frame_counter % K == 0:
            self.new_output()
    def show_frame(self):
        # Convert to grayscale and display frames
        if self.status:
            cv2.imshow('grayscale frame', self.frame_tr)
        # Press 'q' on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)
    def close(self):
        self.capture.release()
        self.output_video.release()
        cv2.destroyAllWindows()
        exit(1)

    def save_frame(self):
        # Save grayscale frame into video output file
        if self.status: # self.capture.isOpened():
            self.output_video.write(self.frame_tr)
        else:
            print('Capure stream is closed')

def run(video_src, video_out=None, split=-1, transform='n2v', plot='n', gray='y'):
    '''
    run default video to video
    '''
    if video_out is None:
        video_out = os.path.dirname(video_src)
        video_out = os.path.join(video_out,'converted.avi')
    if transform == 'n2v':
        # creates the transformation
        if gray=='y':
            transform = PipeLine([ToGray(),N2VDenoiser()])
        else:
            transform = N2VDenoiser()
    else:
        transform = None

    video_stream_widget = VideoToVideo(video_src, output_path=video_out, split=split, transform=transform)
    print('stop convertion by pressing q')
    n_frames = int(video_stream_widget.capture.get(7))
    for _ in tqdm(range(n_frames)):
        if video_stream_widget.capture.isOpened():
            try:
                video_stream_widget.update()
                if plot == 'y':
                    video_stream_widget.show_frame()
                video_stream_widget.save_frame()
            except AttributeError:
                pass
        else:
            video_stream_widget.close()
    video_stream_widget.close()

class ToGray(object):
    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert to gray avi videos.')
    parser.add_argument('--target', metavar='target', type=str,
                    help='target avi video full path')
    parser.add_argument('--output', metavar='output', type=str,
                    help='output avi video full path')
    parser.add_argument('--plot', metavar='plot', type=str, default='y', 
                    help='show video during convertion flag (y(default), or n))')
    parser.add_argument('--split', metavar='split', type=int, default=-1,
                    help='split videos in 1 minute at 30fps. minus one means no split (default)')
    parser.add_argument('--denoiser', metavar='denoiser', type=str, default=None,
                    help='Denoiser call method to remove noise from each image. Options: Contrast, N2V, None(default))')
    parser.add_argument('--gray', metavar='gray', type=str, default='y',
                    help='convert to gray flag ( y or n , default=y)')
    args = parser.parse_args()
    video_src = args.target 
    print(video_src)
    # creates the transformation pipeline
    transforms = []

    if args.gray == 'y':
        to_gray = ToGray()
        transforms.append(to_gray)
    else:
        to_gray = None

    if args.denoiser == 'N2V':
        denoiser = N2VDenoiser()
        transforms.append(denoiser)
    elif args.denoiser == 'Contrast':
        denoiser = ContrastDenoiser()
        transforms.append(denoiser)
    else:
        denoiser = None

    if len(transforms)>0:
        transform = PipeLine(transforms=transforms)
    else:
        transform = None

    video_stream_widget = VideoToVideo(video_src, output_path = args.output, split=args.split, transform=transform)
    print('stop convertion by pressing q')
    while video_stream_widget.capture.isOpened():
        try:
            video_stream_widget.update()
            if args.plot == 'y':
                video_stream_widget.show_frame()
            video_stream_widget.save_frame()
        except AttributeError:
            pass
