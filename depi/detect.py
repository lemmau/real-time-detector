# USAGE (from project's root directory)
# python3 main.py --detect [source]
import cv2
import numpy as np
from PIL import Image
from PredictedClass import ClassList
from IAModel import IAModel
import argparse
from collections import OrderedDict

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detect", required=False, help="detect video or image", default='image')
args = vars(ap.parse_args())

# Load model checkpoint
model = IAModel('/var/www/real-time-detector/core/models/checkpoint_ssd300_complete.pth.tar(E1000)')

objectDetectionConfig = OrderedDict({
        "Barbijo": True,
        "Proteccion ocular": True,
        "Mascara": False
    })

shouldDisableFaceMask = objectDetectionConfig['Barbijo'] or objectDetectionConfig['Proteccion ocular']
shouldDisableGlassesAndMask = objectDetectionConfig['Mascara']

elements = OrderedDict({key: {'elementName': key, 'isChecked': value} for key, value in objectDetectionConfig.items()})


# Use to run SSD300 on image
if args["detect"] == "image":
    img_path = '/var/www/real-time-detector/core/data/test_data/3.jpg'
    #img_path = '/home/psh/Downloads/image.jpeg'
    original_image = Image.open(img_path, mode='r')
    result = model.detect(original_image, min_score=0.2, max_overlap=0.000000000000001, max_objects=200, elementsConfiguration=elements)
    result.show()

# Use to run SSD300 on webcam
if args["detect"] == "video":
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        original_image = Image.fromarray(frame)
        prediction = model.detect(original_image, min_score=0.6,
                            max_overlap=0.1, max_objects=100, elementsConfiguration=elements)

        cv2.imshow('Video', np.array(prediction))

        # Se espera la tecla 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # se liberan los recursos de la camara
    video_capture.release()
    cv2.destroyAllWindows()
