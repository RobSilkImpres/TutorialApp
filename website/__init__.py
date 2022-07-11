from flask import Flask
import os
import logging
from .dbc import TransactionManager

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = 'SECRET'
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
    