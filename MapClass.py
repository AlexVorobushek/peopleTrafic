from textwrap import fill
from PIL import Image, ImageDraw, ImageFont
import json

from TrigonometryClass import Trigonometry as tr

from params import camera_params


class MapClass:
    def __init__(self, camera_params: dict) -> None:
        self.camera_params = camera_params
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2

        self.widht = int((tr.cos(alpha)*camera_params['captureWidth'])/tr.cos(alpha+beta))
        self.height = int(((tr.cos(alpha)*tr.tan(alpha+beta)-tr.sin(alpha)) /
                       (2*tr.sin(beta/2)))*camera_params['captureHeight'])
        self.peoples = []
    
    def projectPointOntoMap(self, point: tuple) -> tuple:
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2
        captureHeight = self.camera_params['captureHeight']
        captureWidth = self.camera_params['captureWidth']

        pointY = point[1]
        pointX = point[0]

        newPointY = pointY * (tr.cos(alpha)*tr.tan(alpha+beta) - tr.sin(alpha))/(2*tr.sin(beta/2))
        newPointX = (pointY/captureHeight)*(self.widht-captureWidth)/2 + \
         (((captureHeight-pointY)/captureHeight)*(tr.cos(alpha)/tr.cos(alpha+beta)-1)+1)*pointX

        coors = int(newPointX), int(newPointY)
        return coors
    
    def draw(self):
        camera_capture_width = self.camera_params['captureWidth']
        camera_capture_heigth = self.camera_params['captureHeight']

        img = Image.new("RGB", (self.widht, self.height), (50, 50, 50))
        d = ImageDraw.Draw(img,)
        d.polygon(((0, 0), (self.widht, 0), self.projectPointOntoMap((camera_capture_width, camera_capture_heigth)), self.projectPointOntoMap((0, camera_capture_heigth))), fill=(100, 100, 100))

        for x, y in self.peoples:
            # d.point((x, y), (255, 255, 255))
            d.ellipse((x-3, y-3, x+3, y+3), (255, 255, 255))

        img.save('images/map.jpg')
    
    def __str__(self) -> str:
        return json.dumps(self.peoples)
    
    def add_point_at_map(self, point):
        self.peoples.append(point)

    @staticmethod
    def activate():
        return MapClass(camera_params)
