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
from datetime import datetime, timedelta
import time
import calendar

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
    scheduler.add_job(triggerEmailSender, 'cron', second=30, args=[frequency, datetime.today()])
    scheduler.start()

    return jsonify('{"status":"ok, "message": "Cron successfully triggered"}')

def triggerEmailSender(frecuency, now):
    endDay = now.strftime("%Y-%m-%d")
    startDay = now - timedelta(days = 7) if frecuency['frecuency'] == 'weekly' else monthdelta(now, -1)
    startDay = startDay.strftime("%Y-%m-%d")

    sql = f"""SELECT date_format(dr.day, '%%H') hour, dc.name, dr.events FROM DailyReport dr
            JOIN DetectedClass dc ON dc.id = dr.detectedClassId
            WHERE date_format(dr.day, '%%Y-%%m-%%d') >= '{startDay}'
            AND date_format(dr.day, '%%Y-%%m-%%d') <= '{endDay}'
            ORDER BY dr.day"""

    queryResult = db.engine.execute(sql)
    jsonObject = {}

    for row in queryResult:
        className = row['name']

        if className not in jsonObject:
            jsonObject[className] = {'x': [], 'y': [], 'name': className}

        jsonObject[className]['x'].append(row['hour'])
        jsonObject[className]['y'].append(row['events'])

    SendMail.sendMailTo(['belloriniagustin@gmail.com'], 'subject', jsonObject.__str__())
    print('Tick! The time is: %s' % datetime.now())

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])

    return date.replace(day=d,month=m, year=y)

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
