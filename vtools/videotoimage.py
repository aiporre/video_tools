import cv2
import argparse
import os
from tqdm import tqdm


class VideoToImage(object):
    def __init__(self, src=0, output_path = './', extension = '.jpg'):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        self.output_path = output_path
        self.frame_counter = 0
        # resolution of the video
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        self.n_frames = int(self.capture.get(7))
        self.extension = extension

    def update(self):
        # Read the next frame
        if self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            self.frame_counter +=1

    def show_frame(self):
        # Convert to grayscale and display frames
        if self.status:
            cv2.imshow('frame', self.frame)

        # Press 'q' on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save grayscale frame into video output file
        if self.status: # self.capture.isOpened():
            filename = os.path.join(self.output_path,"frame_"+str(self.frame_counter) + self.extension)
            cv2.imwrite(filename, self.frame)

    def close(self, exit=False):
        self.capture.release()
        cv2.destroyAllWindows()
        if exit:
            exit(1)


class VideoToGrayImage(VideoToImage):
    def __init__(self, src=0, output_path = './', extension = '.jpg'):
        super(VideoToGrayImage,self).__init__(src=src, output_path = output_path, extension = extension)

    def update(self):
        super().update()
        if self.status:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)


def run(video_src, output_path=None, extension ='.png', plot='y'):
    '''
    run default video to image
    '''
    if output_path is None:
        output_path = os.path.dirname(video_src)
        output_path = os.path.join(output_path,'video_images')
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    video_stream_widget = VideoToGrayImage(video_src, output_path = output_path, extension = extension)
    if plot == 'y':
        print('stop convertion by pressing q')
    for _ in tqdm(range(video_stream_widget.n_frames)):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert to gray avi videos.')
    parser.add_argument('--target', metavar='target', type=str,
                    help='target avi video full path')
    parser.add_argument('--output', metavar='output', type=str,
                    help='output path where the images are saved')
    parser.add_argument('--plot', metavar='plot', type=str, default='y', 
                    help='show video during convertion flag (y(default), or n))')
    parser.add_argument('--extension', metavar='extension', type=str, default='.jpg',
                    help='extension of the imamge output (default: .jpg)')
    args = parser.parse_args()
    video_src = args.target 
    print(video_src)
    video_stream_widget = VideoToGrayImage(video_src, output_path = args.output, extension = args.extension)
    print('stop convertion by pressing q')
    while video_stream_widget.capture.isOpened():
        try:
            video_stream_widget.update()
            if args.plot == 'y':
                video_stream_widget.show_frame()
            video_stream_widget.save_frame()
        except AttributeError:
            pass
