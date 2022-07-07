from .dbc import transactionManager
from pocaLogging import lambdaHandler

def initializeDB():
    lambdaHandler("Beginning DB Initialization.")
    transactionManager.executeSQLFile('schema.sql')
    lambdaHandler("DB Initialization Complete.")