from flask import Flask
from flask.logging import default_handler
from .dbc import TransactionManager
import os
import logging


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = 'SECRET'
    #Adds the handler to the application
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    app.logger.setLevel(logging.DEBUG)

    debug_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/debug.log')
    info_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/info.log')
    error_file_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/error.log')

    debug_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setLevel(logging.INFO)
    error_file_handler.setLevel(logging.ERROR)

    debug_file_handler.setFormatter(formatter)
    info_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)
    
    app.logger.addHandler(debug_file_handler)
    app.logger.addHandler(info_file_handler)
    app.logger.addHandler(error_file_handler)
    
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
    