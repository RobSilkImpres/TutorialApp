from .dbc import transactionManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def initializeDB():
    logger.info("Beginning DB Initialization.")
    transactionManager.executeSQLFile('schema.sql')
    logger.info("DB Initialization Complete.")