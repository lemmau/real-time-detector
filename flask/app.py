from flask import Flask

app = Flask(__name__, template_folder='static', static_folder="static")

import routes 

app.run()
