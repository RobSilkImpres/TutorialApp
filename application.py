from flask import Flask, render_template

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Sup'