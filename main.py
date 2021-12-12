from MapClass import MapClass
from CameraClass import CameraClass
from DetectorClass import DetectorClass
from DBClass import DBClass

import time

print('\033[33mACTIVATING...\033[0m')
# определение
camera = CameraClass.activate()
detector = DetectorClass.activate()
visibility_map = MapClass.activate()
db = DBClass.activate()

def new_imprinting():
    picture = camera.get_image()

    points = detector.detect(picture)
    visibility_map.update_points_at_map(*points)
    
    db.new_record(map=visibility_map)

print('\033[33mSTART\033[0m')
while True:
    new_imprinting()
    print('\033[32mIMPINTED\033[0m')
    # time.sleep(10*60)

camera.close()
