from flask import Flask, render_template, Response
from src.Video import Video

app = Flask(__name__, template_folder='static', static_folder="static")

app.config.from_object('config')


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/video_feed')
def video():
    return Response(Video.getFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run()
