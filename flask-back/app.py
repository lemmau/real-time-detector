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
from collections import OrderedDict

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins='*')
app.config["socketIo"] = socketIo
app.config["clients"] = []
app.config['JSON_SORT_KEYS'] = False
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


@app.route('/video_feed')
def video():
    elementsConfig = json.loads(getConfiguration().get_data().decode("utf-8"))
    return Response(Video.getFrame(model=realTimeDetector, elementsConfiguration=elementsConfig, app=app), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/configuration', methods=['GET'])
def getConfiguration():
    objectDetectionConfig = OrderedDict(app.config['objectDetection'])

    shouldDisableFaceMask = objectDetectionConfig['Barbijo'] or objectDetectionConfig['Proteccion ocular']
    shouldDisableGlassesAndMask = objectDetectionConfig['Mascara']

    elements = OrderedDict({key: {'elementName': key, 'isChecked': value} for key, value in objectDetectionConfig.items()})
    elements["Barbijo"]['isDisabled'] = shouldDisableGlassesAndMask
    elements["Proteccion ocular"]['isDisabled'] = shouldDisableGlassesAndMask
    elements["Mascara"]['isDisabled'] = shouldDisableFaceMask
    elements["soundAlarm"] = app.config['soundAlarm']

    return jsonify(elements)

@app.route('/configuration/stats', methods=['GET'])
def getConfigurationStats():
    config = OrderedDict()
    config['sendEmails'] = app.config['sendEmails']
    config['frequency'] = app.config['frequency']
    
    return jsonify(config)

@app.route('/configuration/stats', methods=['POST'])
def setConfigurationStats():
    requestData = request.json
    app.config['sendEmails'] = requestData['sendEmails']
    app.config['frequency'] = requestData['frequency']

    return jsonify('{"status":"ok, "message": "Stats Configuration Updated"}')

@app.route('/configuration', methods=['POST'])
def setConfiguration():
    requestData = request.json

    app.config['soundAlarm'] = requestData['soundAlarm']
    del requestData['soundAlarm']
    app.config['objectDetection'] = requestData

    return jsonify('{"status":"ok, "message": "Configuration Changed"}')

@app.route('/loadCron', methods=['POST'])
def setCron():
    frequency = request.json
    print(frequency)

    selectedDayOfWeek = Cron.translateDayOfWeek(frequency['propiedadAdicional']) or '*'
    selectedDayOfMonth = Cron.calculateDayOfMonth(frequency['propiedadAdicional']) or '*'
    cron = Cron(date=datetime.today().strftime("%Y-%m-%d"), day_of_week=selectedDayOfWeek, day=selectedDayOfMonth, hour=frequency['hora'], isDeleted=False)

    if scheduler.get_job(EMAIL_SENDER_CRON_ID):
        scheduler.remove_job(EMAIL_SENDER_CRON_ID)
        
    scheduler.add_job(EmailSender.triggerEmailSender, 'cron', day=selectedDayOfMonth, day_of_week=selectedDayOfWeek, hour=frequency['hora'], args=[frequency, datetime.today(), db, app], id=EMAIL_SENDER_CRON_ID)

    save(session, cron)

    app.config["sendEmails"] = "true"

    for prop in frequency:
        app.config['frequency'][prop] = frequency[prop]

    return jsonify('{"status":"ok, "message": "Cron successfully triggered"}')

@app.route('/removeCron', methods=['GET'])
def removeCron():
    scheduler.remove_job(EMAIL_SENDER_CRON_ID)
    app.config["sendEmails"] = "false"

    return jsonify('{"status":"ok, "message": "Cron successfully removed"}')

@app.route('/statistic/<date>', methods=['GET'])
def getStatistic(date):

    statisticsData = getStatisticsByDate(db, date)

    jsonObject = {}

    for row in statisticsData:
        className = row['name']

        if className not in jsonObject:
            jsonObject[className] = {'x': [], 'y': [], 'name': className}

        jsonObject[className]['x'].append(row['hour'])
        jsonObject[className]['y'].append(row['events'])

    return jsonify(list(jsonObject.values()))

@app.route('/emails', methods=['GET'])
def getEmails():
    return jsonify(list(getAllEmailsAvailables(session, app)))

@app.route('/emails', methods=['POST'])
def saveNewEmail():
    currentEmails = list(getAllEmails(session, app))
    email = request.json
    print(email)

    if any(e.email == email for e in currentEmails):
        restoreEmail(session, email)

        return jsonify('{"status":"ok, "message": "{email} sucessfully restored"}')
    else:
        emailObject = Email(email)
        save(session, emailObject)

        return jsonify('{"status":"ok, "message": "{email} sucessfully saved"}')

@app.route('/removeEmail', methods=['POST'])
def deleteEmails():
    email = request.json
    print(email)
    # emailObject = Email(email, True)

    deleteEmail(session, email)
    
    return jsonify('{"status":"ok, "message": "{email} sucessfully deleted"}')
