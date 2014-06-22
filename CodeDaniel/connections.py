class connection():

    def __init__(self):
        self.connections = []

    def addConnection(self, UserObject):
        self.connections.append(UserObject)

    def removeConnection(self, UserObject):
        self.connections.remove(UserObject)

    def printConnections(self):
        print(self.connections)