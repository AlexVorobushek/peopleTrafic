from imageai.Detection import ObjectDetection
import os
import requests

from local_params import detector_params

MODEL_NAME = 'resnet50_coco_best_v2.1.0.h5'
MODEL_YD_DIRECTORY = 'PeopleTrafic'


class DetectorClass:
    def __init__(self, model_directory='', output_image_path='img_detected.jpg') -> None:
        self.model_path = os.path.join(model_directory, MODEL_NAME)
        # self.create_detector()
        if not os.path.exists(self.model_path):
            self.download_model()
        
        self.create_detector()

        self.output_image_path = output_image_path

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
        detections = list(map(lambda d: (d['box_points'][0], d['box_points'][3]), detections))
        return detections

    def create_detector(self):
        self.model = ObjectDetection()
        self.model.setModelTypeAsRetinaNet()
        self.model.setModelPath(self.model_path)
        self.model.loadModel()

    def download_model(self):
        print('START INSTALLING MODEL...')
        token = 'AQAAAAAqbTNeAAd5R4qqZEksGU-emzIVjSUAerM'
        headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + token
        }

        params = {
            'path': f"{MODEL_YD_DIRECTORY}/{MODEL_NAME}"
        }

        url = "https://cloud-api.yandex.net/v1/disk/resources/download"
        r = requests.get(url=url, params=params, headers=headers)
        res = r.json()
        
        with open(self.model_path, 'wb') as out_stream:
            download = requests.get(res['href'], stream=True)
            for i in download.iter_content(1024):
                out_stream.write(i)
        
        print('INSTALLED')

    @staticmethod
    def activate():
        return DetectorClass(**detector_params)
