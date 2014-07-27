import socketserver
import parsing
import sqlite3

connections = []


class User(socketserver.BaseRequestHandler):
# This class represents one TCP connection of client
# Every time a user connects, an Object of this class is created for the connection
        
    def handle(self):
        # This gets executed after the setup() function.
        # It is executed until the connection is closed => endless loop
        while True:
            # Receive one string
            try:
                userrequest = self.getString()
            except:
                break
            # print(userrequest)
            # Parse string
            ok = self.parse(userrequest)
            # On error close the connection
            if not ok:
                self.request.close()
                break
        
    def parse(self, request):
        # Parse command
        if 'REGISTER' in request:
            ok = parsing.registerHandle(self, request)
        elif 'USER' in request:
            ok = parsing.userHandle(self, request, connections)
        # Check for GETLIST command, must not be executed if user is not yet online
        elif 'GETLIST' in request:
            if self.online == False:
                self.sendString("AUTHENTIFICATION ERR\r\n")
                ok = True
            else:
                ok = parsing.getListHandle(self)
        elif 'MKGRP' in request:
            parsing.mkgrpHandle(self, request)
        elif 'GETGRPS' in request:
            parsing.getgrpsHandle(self, request)
        elif 'GETGRPMBRS' in request:
            parsing.getgrpmbrsHandle(self, request)
        elif 'UPDATEGROUP' in request:
            parsing.updateGrpHandle(self, request, connections)
        elif 'SENDMSG' in request:
            parsing.sendMsgHandle(self, request, connections)
        elif 'PULLMSGS' in request:
            parsing.pullMsgsHandle(self)
        elif 'FORGOTPASS' in request:
            parsing.forgotPassHandle(self, request)
        # Check for QUIT command
        elif request == "QUIT\r\n":
            self.setOnline(False)
            self.sendString("QUIT OK\r\n")
            self.request.close()
            return False
        # If command not known return INVALID COMMAND
        else:
            try:
                self.sendString("INVALID COMMAND\r\n")
            except:
                #self.setOnline(False)
                #self.request.close()
                print("User "+str(self.ID)+" closed connection")
                return False
        return True
    
    # Waits for one TCP transmission and returns the string
    def getString(self):
        s = self.request.recv(8192)
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
        
    # Stores one message in the DB for later delivery
    def storeMsg(self, sender_uid, uid, gid, msg):
        self.c.execute("INSERT into messages (sender_UID, UID, GID, message) VALUES (?, ?, ?, ?)", (sender_uid, uid, gid, msg))
        self.db.commit()
    
    # Pushes all messages with the user as target, to the client
    def pushMsgs(self):
        self.c.execute("SELECT ID, sender_UID, UID, GID, message, pushed FROM messages WHERE UID=? AND pushed=0", (self.ID,))
        for row in self.c.fetchall():
            msg = "DLVMSG\r\n"
            msg += "GID:"+str(row['GID'])+"\r\n"
            msg += "UID:"+str(row['sender_UID'])+"\r\n"
            msg += str(row['message'])
            msg += "\r\n\r\n"
            self.sendString(msg)
            self.c.execute("UPDATE messages SET pushed=1 WHERE ID=?", (row['ID'],))
        self.db.commit()
    
    # Delivers one message to the cleint
    def deliverMsg(self, gid, uid, msg):
        print("deliverMsg")
        message = "DLVMSG\r\n"
        message += "GID:"+str(gid)+"\r\n"
        message += "UID:"+str(uid)+"\r\n"
        message += msg
        message += "\r\n\r\n"
        # print(message)
        self.sendString(message)
        #if self.getString() != "ACK\r\n":
        #    print("Could not deliver message")

    # Sends a list of all users in the DB and their status flag to the client
    def sendList(self, users):
        print("sendList")
        usrlist = 'USRLIST\r\n'
        # Generate list of users, select only coloums 'userid','username' and 'status'
        self.c.execute("SELECT userid, username, status FROM users")
        # For each user send userid, username and status
        for row in self.c.fetchall():
            usrlist += "UID:"+str(row[0])+","+row[1]+","+row[2]+"\r\n"
        # Terminate list
        usrlist += ("\r\n")
        # Catch an exception if no user is registered
        try:
            for user in users:
                user.sendString(usrlist)
        except:
            print("First user logged on")

    # Update the userlist of all connected clients
    def updateUserLists(self):
        print("updateUserLists")
        usrlist = 'USRLIST\r\n'
        # Generate list of users, select only coloums 'userid','username' and 'status'
        self.c.execute("SELECT userid, username, status FROM users")
        # For each user send userid, username and status
        for row in self.c.fetchall():
            usrlist += "UID:"+str(row[0])+","+row[1]+","+row[2]+"\r\n"
        # Terminate list
        usrlist += ("\r\n")
        # print(connections)
        try:
            for user in connections:
                if user.online == True:
                    user.sendString(usrlist)
        except:
            pass
                 
    def setup(self):
        # This gets executed at creation of the class
        # Create SQLite database connection and create a cursor for the DB
        self.db = sqlite3.connect('mysims.sqlite')
        self.db.row_factory = sqlite3.Row
        self.c = self.db.cursor()
        # Set the user status to offline, because the user is not yet authentificated
        self.online = False
        self.ID = None
        self.WebUI = False
        # Add user to the connection list
        connections.append(self)
        # print(connections)

    # This is executed on client disconnect
    def finish(self):
        self.setOnline(False)
        self.updateUserLists()
        self.db.close()
        connections.remove(self)

# Set all users to offline before server start
db = sqlite3.connect('mysims.sqlite')
db.row_factory = sqlite3.Row
c = db.cursor()
c.execute("UPDATE users SET status=0 WHERE status=1")
db.commit()
db.close()
# Create server and bind to port 8075
socketserver.ThreadingTCPServer.allow_reuse_address = True
server = socketserver.ThreadingTCPServer(("", 8075), User)
server.serve_forever()
