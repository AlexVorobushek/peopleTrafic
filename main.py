from MapClass import MapClass
from CameraClass import CameraClass
from DetectorClass import DetectorClass
from DBClass import DBClass

import time

print('ACTIVATING...')
# определение
camera = CameraClass.activate()
detector = DetectorClass.activate()
visibility_map = MapClass.activate()
db = DBClass.activate()

def new_imprinting():
    picture = camera.get_image()

    points = detector.detect(picture)
    for point in points:
        visibility_map.add_point_at_map(
            visibility_map.projectPointOntoMap(point)
        )
    
    db.new_record(map=visibility_map)

print('START')
# while True:
new_imprinting()
print('IMPINTED')
# time.sleep(10*60)

camera.close()
