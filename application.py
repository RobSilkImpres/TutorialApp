from flask import Flask, render_template
from werkzeug.exceptions import abort
import requests

# EB looks for an 'application' callable by default.
application = Flask(__name__, template_folder="templates", static_folder="static")
app = application

@application.route('/')
def index():
    return render_template('index.html')

# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()