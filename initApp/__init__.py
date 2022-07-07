import os
import logging
from .dbc import transactionManager

class engine:
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
    def initializeDB(self):
        self.lambda_handler("Beginning DB Initialization.")
        transactionManager.executeSQLFile('schema.sql')
        self.lambda_handler("DB Initialization Complete.")

    def lambda_handler(self, event):
        self.logger.info('## ENVIRONMENT VARIABLES')
        self.logger.info(os.environ)
        self.logger.info('## EVENT')
        self.logger.info(event)
        
    def returnLogger(self):
        return self.logger