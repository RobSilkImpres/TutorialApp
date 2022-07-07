from flask import Flask
from werkzeug.exceptions import abort
from website import create_app
import pymysql
from dbinit import init_db

# EB looks for an 'application' callable by default.
application = create_app()
app = application

# run the app.
if __name__ == "__main__":
    application.debug = True
    init_db.initializeDB
    application.run()