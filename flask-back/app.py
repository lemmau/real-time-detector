import os
import json
from flask import Flask, Response
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList

app = Flask(__name__)

configFile = os.path.abspath(os.getcwd()) + '/config/config.json'

with open(configFile) as file:
    config = json.load(file)

app.config.update(config)

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'without_mask', '#e6194B')

maskDetector = IAModel(config['ia']['modelPath'], classes)

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(model=maskDetector), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/configuration', methods=['POST'])
def setConfiguration():
    pass
