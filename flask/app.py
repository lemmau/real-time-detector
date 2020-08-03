import sys
sys.path.insert(0, '/var/www/real-time-detector/commons')
import os
import json
from flask import Flask, render_template, Response
from src.Video import Video
from IAModel import IAModel
from PredictedClass import ClassList

app = Flask(__name__, template_folder='static', static_folder="static")

configFile = os.path.abspath(os.getcwd()) + '/config/config.json' 
print(configFile)
with open(configFile) as file:
    config = json.load(file)

classes = ClassList()
classes.addClass(0, 'background', '#ffffff')
classes.addClass(1, 'with_mask', '#3cb44b')
classes.addClass(2, 'without_mask', '#e6194B')

maskDetector = IAModel('/var/www/real-time-detector/core/checkpoint_ssd300_kaggle.pth.tar', classes)

@app.route('/')
@app.route('/configuration')
@app.route('/camera')
@app.route('/statistics')
@app.route('/webcam')
def hello_world():
    return render_template('index.html')

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(model=maskDetector), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run()
