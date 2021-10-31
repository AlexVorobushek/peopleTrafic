import cv2, numpy

from Exceptions import NoCameraError

class CameraClass:
    def __init__(self, cameraID=0) -> None:
        self.video = cv2.VideoCapture(cameraID)
    
    def get_image(self) -> numpy.array:
        check, frame = self.video.read()
        if not check:
            raise NoCameraError('Please check camera connection')
        return frame
    
    def close(self):
        self.video.release()
