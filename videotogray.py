import cv2
import argparse

class VideoToGray(object):
    def __init__(self, src=0, output_path = 'output.avi', split=-1):
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
        if self.split>0 and self.frame_counter % K == 0:
            self.new_output()
    def show_frame(self):
        # Convert to grayscale and display frames
        if self.status:
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
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
            self.output_video.write(self.gray)
        else:
            print('Capure stream is closed')

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
    args = parser.parse_args()
    video_src = args.target 
    print(video_src)
    video_stream_widget = VideoToGray(video_src, output_path = args.output, split=args.split)
    print('stop convertion by pressing q')
    while video_stream_widget.capture.isOpened():
        try:
            video_stream_widget.update()
            if args.plot == 'y':
                video_stream_widget.show_frame()
            video_stream_widget.save_frame()
        except AttributeError:
            pass
