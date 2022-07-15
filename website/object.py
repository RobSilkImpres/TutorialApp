from .persistance import PersistanceManager
import datetime

class Object(PersistanceManager):
    persistanceMapping = {
        "classCode" : "classCode",
        "createTime" : "createTime",
        "editTime" : "editTime"
    }

    classCode = "OBJ"
    def __init__(self, autoGenID=True):
        super().__init__(autoGenID=autoGenID)
        self.isNew=True
        self.createTime = datetime.datetime.now()
        self.editTime = datetime.datetime.now()
        self.classCode = self.classCode

    def read(self, where=''):
        resultDict = {}
        resultSet = []
        attrs = self.dbMap.keys()
        statement = self.createSelectStatement(attrs, where)
        result = self.runSelectStatement(statement)
        for x in result:
            inst = x
            i = 0
            for y in attrs:
                resultDict[y] = result[i]
                i = i + 1
            resultSet.append(resultDict)
        return tuple(result)

    def create(arg):
        obj = Object()
        for x in arg.keys():
            setattr(obj, x, arg[x])
        return obj
    
    def edit(self, newSelf):
        for x in newSelf.keys():
            setattr(self, x, newSelf[x])
        return self
    
    def commit(self):
        attributeMapping = {}
        for x in self.dbMap.keys():
            attributeMapping[x] = getattr(self, x)
        if self.isNew == True:
            query = self.createInsertStatement(attributeMapping)
        else:
            query = self.createUpdateByIDStatement()

        self.runStatement(query)
    
    def getAttrs(self):
        return self.persistanceMapping.keys()
    def getClass():
        return Object.classCode