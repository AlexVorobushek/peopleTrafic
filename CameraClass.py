import cv2
import numpy

from Exceptions import NoCameraError
import params


class CameraClass:
    def __init__(self, **kwargs) -> None:
        self.vertical_viewing_angle = kwargs['vertical_viewing_angle']
        self.horisontal_viewing_angle = kwargs['horisontal_viewing_angle']
        self.tilt_angle = kwargs['tilt_angle']
        self.ID = kwargs['camera_id']
        self.captureHeight = kwargs['captureHeight']
        self.captureWidth = kwargs['captureWidth']

        self.connect()

    def connect(self):
        self.video = cv2.VideoCapture(self.ID)

    def get_image(self) -> numpy.array:
        if params.TEST_AT_STATIC_PICTURE:
            return self.get_substitution_image()

        check, frame = self.video.read()

        if not check:
            raise NoCameraError('Please check camera connection')

        return frame

    def close(self):
        self.video.release()

    @staticmethod
    def activate():
        return CameraClass(**params.camera_params)
    
    def get_substitution_image(self):
        from PIL import Image
        img = Image.open('images/img.jpg')
        img.resize((self.captureWidth, self.captureHeight))
        return img

