from typing import overload
from .object import Object

persistanceMapping = {
        "firstName" : "firstName",
        "lastName" : "lastName",
}

classCode = "ENT"

tableName="CONTACTS"

class Entity(Object):
    def __init__(self):
        super().__init__(True)

    def create(arg):
        obj = Entity()
        for x in arg.keys():
            setattr(obj, x, arg[x])
        return obj
    @overload
    def create():
        obj = Entity()
        return obj