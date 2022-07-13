from .persistance import PersistanceManager
import datetime

class Object(PersistanceManager):
    persistanceMapping = {
        "classCode" : "classCode"
    }

    classCode = "OBJ"
    def __init__(self, autoGenID=True):
        super().__init__(autoGenID=autoGenID)
        self.isNew=True
        self.createTime = datetime.datetime.now()
        self.editTime = datetime.datetime.now()
        self.classCode = self.classCode

    def read(self, where=''):
        attrs = self.dbMap.keys()
        statement = self.createSelectStatement(attrs, where)
        result = self.runStatement(statement)
        return result

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
            self.info("Getting Attribute " + x)
            attributeMapping[x] = getattr(self, x)
        if self.isNew == True:
            statement = self.createInsertStatement(attributeMapping)
        else:
            statement = self.createUpdateByIDStatement()

        #self.runStatement(statement)
    
    def getAttrs(self):
        return self.persistanceMapping.keys()
    def getClass():
        return Object.classCode