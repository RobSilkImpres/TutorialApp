from flask import Flask
from werkzeug.exceptions import abort
from website import create_app
from initApp import engine

# EB looks for an 'application' callable by default.
application = create_app()
eng = engine()
app = application

# run the app.
if __name__ == "__main__":
    application.debug = True
    eng.lambda_handler("Application starting")
    eng.initializeDB()
    application.run()