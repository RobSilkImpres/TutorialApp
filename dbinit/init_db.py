from .dbc import transactionManager

def initializeDB():
    transactionManager.executeSQLFile('schema.sql')