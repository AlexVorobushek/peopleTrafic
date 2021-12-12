from textwrap import fill
import json

from TrigonometryClass import Trigonometry as tr
from DBClass import DBClass

camera_params = DBClass.activate().get_camera_params()


class MapClass:
    def __init__(self, camera_params: dict) -> None:
        self.camera_params = camera_params
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2

        self.widht = int((tr.cos(alpha)*camera_params['capture_width'])/tr.cos(alpha+beta))
        self.height = int(((tr.cos(alpha)*tr.tan(alpha+beta)-tr.sin(alpha)) /
                       (2*tr.sin(beta/2)))*camera_params['capture_height'])
        self.peoples = []
    
    def projectPointOntoMap(self, point: tuple) -> tuple:
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2
        captureHeight = self.camera_params['capture_height']
        captureWidth = self.camera_params['capture_width']

        pointY = point[1]
        pointX = point[0]

        newPointY = pointY * (tr.cos(alpha)*tr.tan(alpha+beta) - tr.sin(alpha))/(2*tr.sin(beta/2))
        newPointX = (pointY/captureHeight)*(self.widht-captureWidth)/2 + \
         (((captureHeight-pointY)/captureHeight)*(tr.cos(alpha)/tr.cos(alpha+beta)-1)+1)*pointX

        coors = int(newPointX), int(newPointY)
        return coors
    
    def __str__(self) -> str:
        return json.dumps(self.peoples)
    
    def update_points_at_map(self, *points):
        self.peoples = []
        for point in points:
            self.peoples.append(self.projectPointOntoMap(point))

    @staticmethod
    def activate():
        return MapClass(camera_params)
