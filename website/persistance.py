from .audit import Audit
import pymysql
import os

class PersistanceManager(Audit):
    def __init__(self, autoGenID=True, tableName=False, delimitor=";", autocommit=True):
        super().__init__()
        self.persistanceMapping = {
            "createTime" : "createTime",
            "editTime" : "editTime"
        }
        if not tableName:
            self.persisted = False
        else:
            self.tableName = tableName
            self.persisted = True
        self.autoGenID = autoGenID
        self.className = 'PersistanceManager'
        self.delimitor = delimitor
        self.autocommit = autocommit
    
    def brStr(self, str):
        return "(" + str + ")"

    def createInsertStatement(self, attributeMap):
        columns = ""
        values = ""
        if isinstance(attributeMap, dict):
            #TODO Add in functions to handle tables that don't have autoGen IDs
            for x in attributeMap.keys():
                values = values + ", " + str(attributeMap[x])
                columns = columns + ", " + x
            statement = "INSERT INTO " + self.tableName + " " + self.brStr(columns) + " VALUES " + self.brStr(values)
            self.debug("SQL: " + statement)
            return statement
        else:
            self.error(self.className + " encountered an error: provided attributeMap is not of type dict")
            self.error(str(attributeMap))
            return False

    def createUpdateByIDStatement(self, attributeMap, id):
        statement = ""
        for x in attributeMap.keys():
            if not statement:
                statement = x
            else:
                statement = statement + x + " = " + attributeMap[x]
        statement = "UPDATE " + self.tableName + " SET " + statement + " WHERE ID = " + str(id)
        self.debug("SQL: " + statement)
        return statement
    
    def createDeleteByIDStatement(self, id):
        statement = "DELETE FROM " + self.tableName + "WHERE ID = " + str(id)
        self.debug("SQL: " + statement)
        return statement
    
    def createSelectStatement(self, attrs, where):
        if isinstance(attrs, dict):
            for x in attrs:
                if not statement:
                    statement = x
                else:
                    statement = statement + ", " + x
        else:
            self.error(self.className + " encountered an error: provided attrs is not of type dict")
            self.error(str(attrs))
            return False
        
        statement = "SELECT " + statement + " FROM " + self.tableName + " WHERE " + where
        self.debug("SQL: " + statement)
        return statement
    def runSelectStatement(self, sql):
        self.logger.debug('SQL: ' + sql)
        if not self.connection.open:
            #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
            self.connection = pymysql.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], password=os.environ['RDS_PASSWORD'], database=os.environ['RDS_DB_NAME'], autocommit=self.autocommit)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception:
            self.error(Exception)
        finally:
            try:
                cursor.close()
            except Exception:
                self.error(Exception)
            try:
                self.connection.close()
            except Exception:
                self.error(Exception)
    def runStatement(self, sql):
        self.logger.debug('SQL: ' + sql)
        if not self.connection.open:
            #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
            self.connection = pymysql.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], password=os.environ['RDS_PASSWORD'], database=os.environ['RDS_DB_NAME'], autocommit=self.autocommit)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            if self.connection.get_autocommit() == False:
                self.connection.commit()
        except Exception:
            if not self.connection.autocommit:
                self.connection.rollback()
            self.error(Exception)
        finally:
            try:
                cursor.close()
            except Exception:
                self.error(Exception)
            try:
                self.connection.close()
            except Exception:
                self.error(Exception)
    
    def parseFile(self, data):
        stmts = []
        DELIMITER = ';'
        stmt = ''
        for lineno, line in enumerate(data):
            if not line.strip():
                continue
            if line.startswith('--'):
                continue
            if 'DELIMITER' in line:
                DELIMITER = line.split()[1]
                continue
            if (DELIMITER not in line):
                stmt += line.replace(DELIMITER, ';')
                continue
            if stmt:
                stmt += line
                stmts.append(stmt.strip())
                stmt = ''
            else:
                stmts.append(line.strip())
        return stmts
    def executeSQLFile(self, filename):
        try:
            data = open(filename, 'r').readlines()
        except Exception:
            self.error(Exception)
        else:
            stmts=self.parseFile(data)
            for stmt in stmts:
                self.runStatement(stmt)