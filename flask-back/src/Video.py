import cv2
import threading
import numpy as np
from PIL import Image

class Video():

    #TODO: implement chose video input, instead the default one
    videoInput = cv2.VideoCapture(0)
    outputFrame = None
    lock = threading.Lock()

    @staticmethod
    def getFrame(model, elementsConfiguration):
        while True:

            _, frame = Video.videoInput.read()
            #Video.outputFrame = imutils.resize(frame, width=400)
            image = Image.fromarray(frame)
            prediction = model.detect(image, min_score=0.2, max_overlap=0.2, max_objects=200, elementsConfiguration=elementsConfiguration)
            
            Video.outputFrame = np.array(prediction)
      
            with Video.lock:
                
                if Video.outputFrame is None:
                    continue

                (flag, encodedImage) = cv2.imencode(".jpg", Video.outputFrame)

                if not flag:
                    continue

            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

