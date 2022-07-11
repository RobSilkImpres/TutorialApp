from flask import Flask
from .logger import debug_file_handler, info_file_handler, error_file_handler
from flask.logging import default_handler
from .dbc import TransactionManager
import os
import logging


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = 'SECRET'
    #Adds the handler to the application
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(debug_file_handler)
    app.logger.addHandler(info_file_handler)
    app.logger.addHandler(error_file_handler)
    
    app.logger.setLevel(logging.DEBUG)
    
    app.logger.debug("Logger Attached.")
    
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

    @app.before_request
    def before_request():
        if request.method == 'GET':
            app.logger.debug(f'{request.method} {request.base_url}: parameters {dict(request.args)}')
        else:
            app.logger.debug(f'{request.method} {request.base_url}: parameters {request.json}')
    