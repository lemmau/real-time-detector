import os
import json
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, send
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList
from core.definitions import CHECKPOINT_NEW as modelPath

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins='*')
# TODO: set cors properly
cors = CORS(app)

clients = []

configFile = os.path.abspath(os.getcwd()) + '/config/config.json'

with open(configFile) as file:
    config = json.load(file)

app.config.update(config)

dbUser = config['database']['username']
dbPassword = config['database']['password']
dbHost = config['database']['host']
dbPort = config['database']['port']
database = config['database']['dbName']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{database}'
db = SQLAlchemy(app)

maskDetector = IAModel(modelPath)


@socketIo.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)

@socketIo.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

def send_message():
    for c in clients:
        print(c)
        socketIo.emit('alarm','esta es la dataaa', room=c)

@app.route('/test_alarm')
def testAlarm():
    send_message()
    return "ok"

@app.route('/video_feed')
def video():
    elementsConfig = json.loads(getConfiguration().get_data().decode("utf-8"))
    return Response(Video.getFrame(model=maskDetector, elementsConfiguration=elementsConfig), mimetype = "multipart/x-mixed-replace; boundary=frame")

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


@app.route('/statistic/<day>', methods=['GET'])
def getStatisticOfToday(day):

    sql = f"""SELECT date_format(dr.day, '%%H') hour, dc.name, dr.events FROM DailyReport dr
              JOIN DetectedClass dc ON dc.id = dr.detectedClassId
              WHERE date_format(dr.day, '%%Y-%%m-%%d') = '{day}'
              ORDER BY dr.day"""

    queryResult = db.engine.execute(sql)

    jsonObject = {}

    for row in queryResult:
        className = row['name']

        if className not in jsonObject:
            jsonObject[className] = {'x': [], 'y': [], 'name': className}

        jsonObject[className]['x'].append(row['hour'])
        jsonObject[className]['y'].append(row['events'])

    return jsonify(list(jsonObject.values()))
