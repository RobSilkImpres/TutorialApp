from flask import Flask
from werkzeug.exceptions import abort
from website import create_app
from dbinit import initializeDB
from pocaLogging import lambdaHandler

# EB looks for an 'application' callable by default.
application = create_app()
app = application

# run the app.
if __name__ == "__main__":
    application.debug = True
    lambdaHandler("Application starting")
    initializeDB()
    application.run()