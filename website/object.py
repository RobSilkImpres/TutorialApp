from .persistance import PersistanceManager
import datetime

class Object(PersistanceManager):
    def __init__(self, autoGenID=True, tableName=False):
        super().__init__(autoGenID, tableName)
        self.isNew=True
        self.createTime = datetime.datetime.now()
        self.persistanceMapping = {
            "createTime" : "createTime"
        }
    
    def read(self, where):
        attrs = self.persistanceMapping.keys()
        statement = self.createSelectStatement(attrs, where)
        result = self.runStatement(statement)
        return result

    def create(self, arg):
        for x in arg.keys():
            setattr(self, x, arg[x])
        return self
    
    def edit(self, newSelf):
        for x in newSelf.keys():
            setattr(self, x, newSelf[x])
        return self
    
    def commit(self):
        attributeMapping = {}
        for x in self.persistanceMapping.keys():
            self.info("Getting Attribute " + x)
            attributeMapping[x] = getattr(self, x)
        if self.isNew == True:
            statement = self.createInsertStatement(attributeMapping)
        else:
            statement = self.createUpdateByIDStatement()

        #self.runStatement(statement)
    
    def getAttrs(self):
        return self.persistanceMapping.keys()