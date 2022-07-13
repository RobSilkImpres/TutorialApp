from .audit import Audit
import mysql.connector
import os

class PersistanceManager(Audit):
    persistanceMapping = {
        "createTime" : "createTime",
        "editTime" : "editTime"
    }

    tableName = ''
    def __init__(self, autoGenID=True, delimitor=";", autocommit=True):
        super().__init__()
        self.dbMap = {}
        for x in self.persistanceMapping.keys():
            self.dbMap[x] = self.persistanceMapping[x]
        if not self.tableName:
            self.persisted = False
        else:
            if isinstance(self.tableName, str):
                self.tableName = self.tableName.upper()
                self.persisted = True
            else:
                error = "Table name " + str(self.tableName) + " is not of type String."
                Audit.raiseCustomError(error)
        self.autoGenID = autoGenID
        self.className = 'PersistanceManager'
        self.delimitor = delimitor
        self.autocommit = autocommit
    
    def createConn(self):
        connection = mysql.connector.connect(
            host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], password=os.environ['RDS_PASSWORD'], database=os.environ['RDS_DB_NAME'], autocommit=self.autocommit
        )
        return connection
    def brStr(self, str):
        return "(" + str + ")"

    def createInsertStatement(self, attributeMap):
        columns = ""
        values = ""
        #TODO Add in functions to handle tables that don't have autoGen IDs
        for x in attributeMap.keys():
            values = values + ", " + str(attributeMap[x])
            columns = columns + ", " + x.upper()
        statement = "INSERT INTO " + self.tableName + " " + self.brStr(columns) + " VALUES " + self.brStr(values)
        Audit.debug("SQL: " + statement)
        return statement

    def createUpdateByIDStatement(self, attributeMap, id):
        statement = ""
        for x in attributeMap.keys():
            if not statement:
                statement = x
            else:
                statement = statement + x.upper() + " = " + str.attributeMap[x]
        statement = "UPDATE " + self.tableName + " SET " + statement + " WHERE ID = " + str(id)
        self.debug("SQL: " + statement)
        return statement
    
    def createDeleteByIDStatement(self, id):
        statement = "DELETE FROM " + self.tableName + "WHERE ID = " + str(id)
        self.debug("SQL: " + statement)
        return statement
    
    def createSelectStatement(self, attrs='*', where=False):
        if attrs == '*':
            statement = '*'
        else:
            for x in attrs:
                if not statement:
                    statement = x
                else:
                    statement = statement + ", " + x
        if not where:
            where = ''
        else:
            where = " WHERE " + where
        statement = "SELECT " + statement + " FROM " + self.tableName + where
        self.debug("SQL: " + statement)
        return statement
    def runSelectStatement(self, sql):
        self.logger.debug('SQL: ' + sql)
        #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
        connection = self.createConn()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            self.error(e)
            raise
        finally:
            try:
                cursor.close()
            except Exception as e:
                self.error(e)
                raise
            try:
                connection.close()
            except Exception as e:
                self.error(e)
                raise
    def runStatement(self, sql):
        self.logger.debug('SQL: ' + sql)
        #Set autocommit to false. Environment variables are pulled from Elastic Beanstalk
        connection = self.createConn()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            if connection.get_autocommit() == False:
                connection.commit()
        except Exception as e:
            if not connection.autocommit:
                connection.rollback()
            self.error(e)
            raise
        finally:
            try:
                cursor.close()
            except Exception as e:
                self.error(e)
                raise
            try:
                connection.close()
            except Exception as e:
                self.error(e)
                raise
    
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
        self.debug("Running script " + filename)
        try:
            conn = self.createConn()
        except Exception as e:
            self.error(e)
            raise
        else:
            try:
                with open(filename, 'r') as f:
                    with conn.cursor() as cursor:
                        result = cursor.execute(f.read(), multi=True)
                    conn.commit()
            except Exception as e:
                self.error(e)
                raise
            finally:
                try:
                    cursor.close()
                except Exception as e:
                    self.error(e)
                    raise
                try:
                    conn.close()
                except Exception as e:
                    self.error(e)
                    raise
                return result