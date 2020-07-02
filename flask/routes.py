from __main__ import app

@app.route('/')
def hello_world():
    return 'Hello, World!'
    