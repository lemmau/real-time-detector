# USAGE (from project's root directory)
# python3 main.py --detect [source]
import cv2
import numpy as np
from PIL import Image
from commons.PredictedClass import ClassList
from commons.IAModel import IAModel
from .. definitions import CHECKPOINT, TEST_DATA_PATH
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detect", required=False, help="detect video or image", default="image")
args = vars(ap.parse_args())

# Load model checkpoint
model = IAModel(CHECKPOINT)

# Use to run SSD300 on image
if args["detect"] == "image":
    img_path = TEST_DATA_PATH + '8.jpg'
    original_image = Image.open(img_path, mode='r')
    
    config = {
        "backendEndpoint": "http://localhost:5000",
        "database": {
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "root",
            "dbName": "real-time-detector" 
        },
        "email": {
            "smptServer": "smtp.gmail.com",
            "smptPort": 587,
            "senderMail": "rtd.notifications@gmail.com",
            "senderPassword": "rtdutn2020"
        },
        "possibleElements": ["Barbijo", "Proteccion ocular", "Mascara"],
        "objectDetection": {
            "Barbijo": "true",
            "Proteccion ocular": "true",
            "Mascara": "false"
        },
        "soundAlarm": "false",
        "sendEmails": "true",
        "frequency": {
            "hora": "00",
            "periodicidad": "Diaria",
            "propiedadAdicional": ""
        }
    }

    result = model.detect(original_image, min_score=0.2, max_overlap=0.5, max_objects=200, elementsConfiguration=config, app=None)
    result.show()

# Use to run SSD300 on webcam
if args["detect"] == "video":
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        original_image = Image.fromarray(frame)
        prediction = model.detect(original_image, min_score=0.6,
                            max_overlap=0.1, max_objects=100)

        cv2.imshow('Video', np.array(prediction))

        # Se espera la tecla 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # se liberan los recursos de la camara
    video_capture.release()
    cv2.destroyAllWindows()
