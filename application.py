from flask import Flask, render_template

# EB looks for an 'application' callable by default.
application = Flask(__name__)
app = application

@application.route('/')
def hello_world():
    return 'Sup'