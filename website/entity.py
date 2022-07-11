from .object import Object

class Entity(Object):
    def __init__(self, firstName, lastName):
        super().__init__(True, "Contacts")
        if not firstName or not lastName:
            self.error("First and Last names cannot be NULL")
        self.firstName = firstName
        self.lastName = lastName