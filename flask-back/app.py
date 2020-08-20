import os
import json
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList
from core.definitions import CHECKPOINT as modelPath

app = Flask(__name__)

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
print(f'mysql://{dbUser}:{dbPassword}@{dbHost}/{database}')
db = SQLAlchemy(app)

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'without_mask', '#e6194B')

maskDetector = IAModel(modelPath, classes)

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(model=maskDetector), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/configuration', methods=['POST'])
def setConfiguration():
    pass
