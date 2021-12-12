import cv2
import numpy

from Exceptions import NoCameraError
from DBClass import DBClass

camera_params = DBClass.activate().get_camera_params()


class CameraClass:
    def __init__(self, **kwargs) -> None:
        self.vertical_viewing_angle = kwargs['vertical_viewing_angle']
        self.horisontal_viewing_angle = kwargs['horisontal_viewing_angle']
        self.tilt_angle = kwargs['tilt_angle']
        self.ID = kwargs['port_id']
        self.captureHeight = kwargs['capture_height']
        self.captureWidth = kwargs['capture_width']

        if camera_params['test_at_static_picture']:
            self.videoClass = SubstitutionImageFromVideo('images/video.mp4')
        else:
            self.connect()

    def connect(self):
        self.video = cv2.VideoCapture(self.ID)
        if not self.video.isOpened():
            raise NoCameraError('Please check camera connection')

    def get_image(self) -> numpy.array:
        if camera_params['test_at_static_picture']:
            return self.get_substitution_image()

        _, frame = self.video.read()
        return frame

    def close(self):
        self.video.release()

    @staticmethod
    def activate():
        return CameraClass(**camera_params)
    
    def get_substitution_image(self):
        from PIL import Image
        self.videoClass.get_frame()
        img = Image.open('images/img.jpg')
        img.resize((self.captureWidth, self.captureHeight))
        return img
        img = self.videoClass.get_frame()
        img.resize((self.captureWidth, self.captureHeight))
        return img

class SubstitutionImageFromVideo:
    def __init__(self, video_name) -> None:
        self.frame_step = 2400
        self.video_name = video_name

        self.connect()
    
    def connect(self):
        self.video = cv2.VideoCapture(self.video_name)
        if not self.video.isOpened():
            raise NoCameraError('Please check exist video')

        fps = self.video.get(cv2.CAP_PROP_FPS)
        est_video_length_minutes = 3
        est_tot_frames = est_video_length_minutes * 60 * fps

        self.desired_frames = self.frame_step * numpy.arange(est_tot_frames) 
        self.i_in_desired_frames = 0
    
    def get_frame(self):
        self.video.set(1, self.desired_frames[self.i_in_desired_frames]-1)   
        self.i_in_desired_frames += 1

        _, frame = self.video.read(1)
        cv2.imwrite('images/img.jpg', frame)
        return frame


