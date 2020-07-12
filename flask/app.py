from flask import Flask, render_template

app = Flask(__name__, template_folder='static', static_folder="static")

app.config.from_object('config')


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
