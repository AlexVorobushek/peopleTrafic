from DetectorClass import DetectorClass
from CameraClass import CameraClass

camera = CameraClass(cameraID=0)
detector = DetectorClass(
    output_image_path='images/img_detected.jpg'
)

print(
    detector.detect(
        camera.get_image()
    )
)

camera.close()