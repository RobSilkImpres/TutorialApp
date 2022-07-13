from .object import Object

persistanceMapping = {
        "firstName" : "firstName",
        "lastName" : "lastName",
        "classCode" : "classCode",
        "createTime" : "createTime",
        "editTime" : "editTime"
}

classCode = "ENT"

tableName="CONTACTS"

class Entity(Object):
    def __init__(self):
        super().__init__(True)

    def create(arg={}):
        obj = Entity()
        for x in arg.keys():
            setattr(obj, x, arg[x])
        return obj