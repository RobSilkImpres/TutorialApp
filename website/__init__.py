from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler
from .dbc import TransactionManager

##Set up the python logger handlers
#Setup instantiate the logger, set the logging level, and set format for the logs
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger.setLevel(logging.INFO)

#Handler Options
#handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
#handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
handler = RotatingFileHandler('/var/log/application.log', maxBytes=1024,backupCount=5)

#Set the handler formatter
handler.setFormatter(formatter)

logging.basicConfig(filename = 'flask-tutorial-v3.log', level='INFO', format = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = 'SECRET'
    #Adds the handler to the application. Required for Elastic Beanstalk
    app.logger.addHandler(handler)
    
    app.logger.info('Application is starting.')
    
    tm = TransactionManager()
    
    #Initialize DB
    app.logger.info("Beginning DB Initialization.")
    tm.executeSQLFile('schema.sql')
    app.logger.info("DB Initialization Complete.")
    
    #Register blueprints to define server paths
    from .views import views
    #from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(auth, url_prefix='/')
    
    return app
    