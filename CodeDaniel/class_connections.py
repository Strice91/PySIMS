class connections():

    def __init__(self):
        self.connections = []
        print("BL bl")

    def addConnection(self, UserObject):
        self.connections.append(UserObject)
        print(self.connections)

    def removeConnection(self, UserObject):
        self.connections.remove(UserObject)

    def getConnections(self):
        return self.connections

    def printConnections(self):
        print(self.connections)