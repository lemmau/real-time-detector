import os
import json
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from flask_socketio import SocketIO, send
from IAModel import IAModel
from PredictedClass import ClassList
from core.definitions import CHECKPOINT_NEW as modelPath, EMAIL_SENDER_CRON_ID
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.Video import Video
from src.EmailSender import EmailSender
from src.Cron import Cron
from src.DBHelper import *
from src.DailyReport import DailyReport
from datetime import datetime

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins='*')
app.config["socketIo"] = socketIo
app.config["clients"] = []
# TODO: set cors properly
cors = CORS(app)

clients = []

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
Session = sessionmaker()
Session.configure(bind=db.engine)
session = Session()

app.app_context().push()

scheduler = BackgroundScheduler()

print('Starting daily report cron')

scheduler.add_job(DailyReport.runSync, 'cron', hour=00, args=[db, session])
scheduler.start()

print('Daily report cron successfully started running everyday at 00h')

@socketIo.on('connect')
def handle_connect():
    app.config["clients"].append(request.sid)

@socketIo.on('disconnect')
def handle_disconnect():
    app.config["clients"].remove(request.sid)

# def throwAlarm():
#     soundAlarmOn = app.config['soundAlarm']
#     for client in app.config["clients"]:
#         socketIo.emit('alarm', {'audio': soundAlarmOn}, room=client)

@app.route('/video_feed')
def video():
    elementsConfig = json.loads(getConfiguration().get_data().decode("utf-8"))
    return Response(Video.getFrame(model=realTimeDetector, elementsConfiguration=elementsConfig, app=app), mimetype = "multipart/x-mixed-replace; boundary=frame")

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

    selectedDayOfWeek = Cron.translateDayOfWeek(frequency['propiedadAdicional']) or '*'
    selectedDayOfMonth = Cron.calculateDayOfMonth(frequency['propiedadAdicional']) or '*'
    cron = Cron(date=datetime.today().strftime("%Y-%m-%d"), day_of_week=selectedDayOfWeek, day=selectedDayOfMonth, hour=frequency['hora'], isDeleted=False)

    scheduler.add_job(EmailSender.triggerEmailSender, 'cron', day=selectedDayOfMonth, day_of_week=selectedDayOfWeek, hour=frequency['hora'], args=[frequency, datetime.today(), db, app], id=EMAIL_SENDER_CRON_ID)

    save(session, cron)

    scheduler.start()

    app.config["sendEmails"] = "true"

    for prop in frequency:
        app.config['frequency'][prop] = frequency[prop]

    return jsonify('{"status":"ok, "message": "Cron successfully triggered"}')

@app.route('/removeCron', methods=['GET'])
def removeCron():
    scheduler.remove_job(EMAIL_SENDER_CRON_ID)
    app.config["sendEmails"] = "false"

    return jsonify('{"status":"ok, "message": "Cron successfully removed"}')

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
