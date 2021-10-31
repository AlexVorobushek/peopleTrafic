from imageai.Detection import ObjectDetection
import os

from numpy.core.defchararray import array

class DetectorClass:
    def __init__(self, model_path='/', output_image_path='img_detected.jpg') -> None:
        self.model = ObjectDetection()
        self.model.setModelTypeAsRetinaNet()
        self.model.setModelPath('resnet50_coco_best_v2.1.0.h5')
        self.model.loadModel()

        self.output_image_path=output_image_path
        print('detector object was created'.upper())
    
    def detect(self, input_image) -> list:
        custom_objects = self.model.CustomObjects(person=True)
        detections = self.model.detectObjectsFromImage(
            input_type='array',
            input_image=input_image,
            output_image_path=self.output_image_path,
            custom_objects=custom_objects,
            minimum_percentage_probability=20,
            display_object_name=False,
            display_percentage_probability=False
        )
        return detections    
