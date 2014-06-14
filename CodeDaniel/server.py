import socketserver
import parsing
import sqlite3

# List of all connections, consists of 'User' objects
connections = []


class User(socketserver.BaseRequestHandler):
# This class presents one TCP connection of client
# Every time a user connects, an Object of this class is created for the connection
        
    def handle(self):
        # This gets executed after the setup() function.
        # It is executed until the connection is closed => endless loop
        while True:
            # Receive one string
            userrequest = self.getString()
            print(userrequest)
            # Parse string
            ok = self.parse(userrequest)
            # On error close the connection
            if not ok:
                self.request.close()
                break
        
    def parse(self, request):
        # Check for REGISTER command
        if 'REGISTER' in request:
            ok = parsing.registerHandle(self, request)
        # Check for USER command
        elif 'USER' in request:
            ok = parsing.userHandle(self, request, connections)
        # Check for PASS command, must not be executed without USER command
        elif 'PASS' in request:
            self.sendString("PASS WITHOUT USER\r\n")
        # Check for GETLIST command, must not be executed if user is not yet online
        elif 'GETLIST' in request:
            if self.online == False:
                self.sendString("ERR\r\n")
                ok = True
            else:
                ok = parsing.getListHandle(self, request)
        # Check for SENDMSG command
        # Check for MKGRP command
        elif 'MKGRP' in request:
            parsing.mkgrpHandle(self)
        elif 'GETGRPS' in request:
            parsing.getgrpsHandle(self)
        elif 'GETGRPMBRS' in request:
            parsing.getgrpmbrsHandle(self)
        elif 'SENDMSG' in request:
            parsing.sendMsgHandle(self, request, connections)
        # Check for QUIT command
        elif request == "QUIT\r\n":
            self.setOnline(False)
            self.sendString("OK\r\n")
            self.request.close()
            return False
        # If command not known return INVALID COMMAND
        else:
            self.request.send(("INVALID COMMAND\r\n").encode('UTF-8'))
        return True
    
    # Waits for one TCP transmission and returns the string
    def getString(self):
        s = self.request.recv(1024)
        return s.decode('UTF-8')

    # Sends one string as TCP transmission
    def sendString(self, string):
        msg = string.encode('UTF-8')
        self.request.send(msg)
    
    # Sets the user status, 'switch' must be True or False
    def setOnline(self, switch):
        # Set object member
        self.online = switch
        # Set status in DB
        self.c.execute("UPDATE users SET status = ? WHERE userid=?", (self.online, self.ID))
        self.db.commit()
                 
    def setup(self):
        # This gets executed at creation of the class
        
        # Create SQLite database connection and create a cursor for the DB
        self.db = sqlite3.connect('mysims.sqlite')
        self.db.row_factory = sqlite3.Row
        self.c = self.db.cursor()
        # Set the user status to offline, because the user is not yet authentificated
        self.online = False
        # Add user to the connection list
        connections.append(self)

    def finish(self):
        self.setOnline(False)
        self.db.close()

# Create server and bind to port 8075
socketserver.ThreadingTCPServer.allow_reuse_address = True
server = socketserver.ThreadingTCPServer(("", 8075), User)
server.serve_forever()