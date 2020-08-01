import os
import json
from flask import Flask, render_template, Response
from src.Video import Video

app = Flask(__name__, template_folder='static', static_folder="static")

configFile = os.path.abspath(os.getcwd()) + '/config/config.json' 
print(configFile)
with open(configFile) as file:
    config = json.load(file)


print(app.config.get('email'))
@app.route('/')
@app.route('/configuration')
@app.route('/camera')
@app.route('/statistics')
@app.route('/webcam')
def hello_world():
    return render_template('index.html')

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run()
