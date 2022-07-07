from multiprocessing import connection
import pymysql

class transactionManager:
    def __init__(self, delimitor=";", autocommit=True):
        #Set autocommit to false
        self.connection = pymysql.connect(host="poca-db.cixxwadsbdjm.us-east-2.rds.amazonaws.com", user="admin", password="password", database="poca", autocommit=autocommit)
        self.delimitor = delimitor
        self.autocommit = autocommit
    
    def runStatement(self, sql):
        if not self.connection.open:
            self.connection = pymysql.connect(host="poca-db.cixxwadsbdjm.us-east-2.rds.amazonaws.com", user="admin", password="password", database="poca", autocommit=self.autocommit)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            if self.connection.get_autocommit() == False:
                self.connection.commit()
        except Exception:
            if not self.connection.autocommit:
                self.connection.rollback()
            print(Exception)
        finally:
            try:
                cursor.close()
            except Exception:
                print(Exception)
            try:
                self.connection.close()
            except Exception:
                print(Exception)
    
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
            print(Exception)
        else:
            stmts=self.parseFile(data)
            for stmt in stmts:
                self.runStatement(stmt)
                
        