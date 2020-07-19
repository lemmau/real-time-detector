import cv2
import threading
import imutils
from imutils.video import VideoStream

class Video():

    # TODO: implement chose video input, instead the default one
    videoInput = VideoStream(src=0).start()
    outputFrame = None
    lock = threading.Lock()

    @staticmethod
    def getFrame():
        while True:

            frame = Video.videoInput.read()
            Video.outputFrame = imutils.resize(frame, width=400)

            with Video.lock:
                
                if Video.outputFrame is None:
                    continue

                (flag, encodedImage) = cv2.imencode(".jpg", Video.outputFrame)

                if not flag:
                    continue

            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

