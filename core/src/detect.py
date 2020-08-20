# USAGE (from project's root directory)
# python3 main.py --detect [source]
import cv2
import numpy as np
from PIL import Image
from commons.PredictedClass import ClassList
from commons.IAModel import IAModel
from .. definitions import CHECKPOINT, TEST_DATA_PATH, BACKGROUND_RGB, WITH_MASK_RGB, WITHOUT_MASK_RGB
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detect", required=True, help="detect video or image")
args = vars(ap.parse_args())

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'with_glasses', '#092FEB')
classes.addClass(3, 'with_mask_and_glasses', '#000000')
classes.addClass(4, 'clean', '#e6194B')

# Load model checkpoint
model = IAModel(CHECKPOINT, classes)

# Use to run SSD300 on image
if args["detect"] == "image":
    img_path = TEST_DATA_PATH + '3.jpg'
    original_image = Image.open(img_path, mode='r')
    result = model.detect(original_image, min_score=0.2, max_overlap=0.5, max_objects=200)
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
