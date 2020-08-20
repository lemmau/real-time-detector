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
classes.addClass(2, 'with_glasses', '#092FEB')
classes.addClass(3, 'with_mask_and_glasses', '#FFF926')
classes.addClass(4, 'clean', '#e6194B')

maskDetector = IAModel(modelPath, classes)

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(model=maskDetector), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/configuration', methods=['GET'])
def getConfiguration():
    objectDetectionConfig = app.config['objectDetection']
    return jsonify(objectDetectionConfig)

@app.route('/configuration', methods=['POST'])
def setConfiguration():

    requestData = request.json
    print(requestData)

    if 'element' not in requestData or 'enable' not in requestData:
        return jsonify('{"status":"error, "message": "\'element\' or \'enable\' not property not found"}')

    element = requestData['element']
    enable = requestData['enable']

    if element not in app.config['possibleElements']:
        return jsonify('{"status":"error, "message": "Element is not allowed"}')

    app.config['objectDetection'][element] = bool(enable)

    return jsonify('{"status":"ok, "message": "Configuration Changed"}')
