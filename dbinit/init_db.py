from .dbc import transactionManager
import logging

logging.basicConfig(level=logging.INFO)

def initializeDB():
    logging.info("Beginning DB Initialization.")
    transactionManager.executeSQLFile('schema.sql')
    logging.info("DB Initialization Complete.")