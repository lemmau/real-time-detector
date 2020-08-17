import os
import json
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList
from core.definitions import CHECKPOINT as modelPath

app = Flask(__name__)
# TODO: set cors properly
cors = CORS(app)

configFile = os.path.abspath(os.getcwd()) + '/config/config.json'

with open(configFile) as file:
    config = json.load(file)

app.config.update(config)

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'without_mask', '#e6194B')

maskDetector = IAModel(modelPath, classes)

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(model=maskDetector), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/configuration', methods=['GET'])
def getConfiguration():
    objectDetectionConfig = app.config['objectDetection']
    return jsonify(objectDetectionConfig)

@app.route('/configuration/<element>/<enable>', methods=['GET'])
def setConfiguration(element:str, enable:str):

    if element not in app.config['possibleElements']:
        return jsonify('{"status":"error, "message": "Element is not allowed"}')

    app.config['objectDetection'][element] = bool(int(enable))

    return jsonify('{"status":"ok, "message": "Configuration Changed"}')
