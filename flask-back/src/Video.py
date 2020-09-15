import cv2
import threading
import numpy as np
from PIL import Image
from core.definitions import MIN_SCORE, MAX_OVERLAP, MAX_OBJECTS

class Video():

    #TODO: implement chose video input, instead the default one
    videoInput = cv2.VideoCapture(0)
    outputFrame = None
    lock = threading.Lock()

    @staticmethod
    def getFrame(model, elementsConfiguration, app):
        while True:

            _, frame = Video.videoInput.read()
            #Video.outputFrame = imutils.resize(frame, width=400)
            image = Image.fromarray(frame)
            prediction = model.detect(image, min_score=MIN_SCORE, max_overlap=MAX_OVERLAP, max_objects=MAX_OBJECTS, elementsConfiguration=elementsConfiguration, app=app)
            
            Video.outputFrame = np.array(prediction)
      
            with Video.lock:
                
                if Video.outputFrame is None:
                    continue

                (flag, encodedImage) = cv2.imencode(".jpg", Video.outputFrame)

                if not flag:
                    continue

            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

