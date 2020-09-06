import os
import json
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList
from core.definitions import CHECKPOINT_NEW as modelPath
from apscheduler.schedulers.background import BackgroundScheduler
from src.SendMail import SendMail
# from src.Email import Email
from datetime import datetime
import time

app = Flask(__name__)
# TODO: set cors properly
cors = CORS(app)

configFile = os.path.abspath(os.getcwd()) + '/config/config.json'

with open(configFile) as file:
    config = json.load(file)

app.config.update(config)

realTimeDetector = IAModel(modelPath)

dbUser = config['database']['username']
dbPassword = config['database']['password']
dbHost = config['database']['host']
dbPort = config['database']['port']
database = config['database']['dbName']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{database}'
db = SQLAlchemy(app)

@app.route('/video_feed')
def video():
    elementsConfig = json.loads(getConfiguration().get_data().decode("utf-8"))
    return Response(Video.getFrame(model=realTimeDetector, elementsConfiguration=elementsConfig), mimetype = "multipart/x-mixed-replace; boundary=frame")

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

@app.route('/loadCron', methods=['POST'])
def setCron():
    frequency = request.json
    print(frequency)

    scheduler = BackgroundScheduler()
    scheduler.add_job(triggerEmailSender, 'cron', hour=11, minute=48, args=[frequency])
    scheduler.start()

    return jsonify('{"status":"ok, "message": "Cron successfully triggered"}')

def triggerEmailSender(frequency):
    SendMail.sendMailTo(['belloriniagustin@gmail.com'], 'subject', 'Message')
    print('Tick! The time is: %s' % datetime.now())
