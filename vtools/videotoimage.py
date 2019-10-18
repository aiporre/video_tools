import cv2
import argparse
import os 

class VideoToGrayImage(object):
    def __init__(self, src=0, output_path = './', extension = '.jpg'):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        self.output_path = output_path
        self.frame_counter = 0
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
        self.extension = extension


    def update(self):
        # Read the next frame 
        if self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            self.frame_counter +=1
        if self.status:
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def show_frame(self):
        # Convert to grayscale and display frames
        if self.status:
            cv2.imshow('grayscale frame', self.gray)

        # Press 'q' on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save grayscale frame into video output file
        if self.status: # self.capture.isOpened():
            filename = os.path.join(self.output_path,"frame_"+str(self.frame_counter) + self.extension)
            cv2.imwrite(filename, self.gray)
            if os.path.exists(filename):
                print('file :', filename, 'created')
            else:
                print('file :', filename, 'failed')
        else:
            print('Capure stream is closed')

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
