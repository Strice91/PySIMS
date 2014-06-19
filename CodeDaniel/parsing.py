import uuid
import time
import hashlib

# This function implements the REGISTER [username] [password] command
def registerHandle(self, request):
    print("registerHandle")
    split = request.split(" ")
    username = split[1].strip()
    password = split[2].strip()
    passhash = hashlib.md5()
    passhash.update(password.encode('UTF-8'))
    # Check if username already in DB
    self.c.execute("SELECT username FROM users WHERE username=?", (username,))
    if not self.c.fetchall() == []:
        self.sendString("USER ERR\r\n")
    else:
        # If username is free add the user to the database
        self.c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, passhash.hexdigest()))
        self.db.commit()
        print("Successfully registered user",username)
        self.sendString("REGISTER OK\r\n")
    return True

# This function implements the USER [username] and PASS [password] command
def userHandle(self, request, connections):
    print("userHandle")
    split = request.split(" ")
    # Get username from request
    username = split[1].strip()
    # Check if user in DB
    self.c.execute("SELECT * FROM users WHERE username=?", (username,))
    login = self.c.fetchone()
    if login == None:
        self.sendString("USER ERR\r\n")
        print("User", username, "not found.")
    else:
        self.sendString("USER OK\r\n")
        # Wait for PASS [password] command
        passcommand = self.getString()
        if not "PASS" in passcommand:
            self.sendString("LOGIN ABORTED\r\n")
        else:
            # Check if received password is ok
            password = passcommand.split(" ")[1].strip()
            passhash = hashlib.md5()
            passhash.update(password.encode('UTF-8'))
            if not passhash.hexdigest() == login[2]:
                self.sendString("PASS ERR\r\n")
                print("User", username, "entered wrong password.")
            else:
                # If password is ok, set the UID, generate SID, set User to 'online' and return OK and SID
                self.ID = login[0]
                for user in connections:
                    if user.online == True and user.ID == self.ID:
                        user.sendString("CLOSING CONNECTION\r\n")
                        user.request.close()
                        print("Closed connection of user", username, "because of multiple login.")
                self.SID = uuid.uuid4().hex
                self.setOnline(True)
                self.sendString("PASS OK\r\nUID:"+str(self.ID)+"\r\nSID:"+str(self.SID)+"\r\n\r\n")
                print("User "+username+" logged in.")
                self.pushMsgs()
                self.sendList(connections)
    return True

# This function implements the GETLIST command
def getListHandle(self, request):
    print("getListHandle")
    self.sendList([self])

def sendList(self, users):
    usrlist = 'USRLIST\r\n'
    # Generate list of users, select only coloums 'userid','username' and 'status'
    self.c.execute("SELECT userid, username, status FROM users")
    # For each user send userid, username and status
    for row in self.c.fetchall():
        usrlist += "UID:"+str(row[0])+","+row[1]+","+row[2]+"\r\n"
    # Terminate list
    usrlist += ("\r\n")
    for user in users:
        user.sendString(usrlist)

# This function implements the MKGRP command
def mkgrpHandle(self, request):
    print("mkgrpHandle")
    # print(request.split("\r\n"))
    userids = request.split("\r\n")[1]
    userids = userids.lstrip("UID:").rstrip("\r\n")
    userids = userids.split(',')
    # print(userids)
    sid = request.split("\r\n")[2]
    sid = sid.lstrip("SID:").rstrip("\r\n")
    # print(sid)
    timestamp = int(time.time())
    self.c.execute("INSERT INTO groups (creationdate) VALUES (?)", (timestamp,))
    self.c.execute("SELECT last_insert_rowid()")
    gid = self.c.fetchone()[0]
    for uid in userids:
        self.c.execute("INSERT INTO groupmembers (GID, UID) VALUES (?, ?)", (gid, uid))
    self.db.commit()
    self.sendString("MKGRP OK\r\nGID:"+str(gid)+"\r\n\r\n")
    print("Created group", gid, "with users", userids)

# This function implements the GETGRPS command
def getgrpsHandle(self, request):
    print("getgrpsHandle")
    sid = request.split("\r\n")[1].lstrip("SID:")
    grplist = "GRPS\r\n"
    self.c.execute("SELECT gid FROM groupmembers WHERE UID=?", (self.ID,))
    for row in self.c.fetchall():
        grplist += "GID:"+str(row[0])+"\r\n"
    grplist += "\r\n"
    self.sendString(grplist)

# This function implements the GETGRPMBRS command
def getgrpmbrsHandle(self, request):
    print("getgrpmbrsHandle")
    print(request.split("\r\n"))
    gid = request.split("\r\n")[1].lstrip("GID:")
    grpmbrs = "MEMBERS\r\n"
    # Get group members from DB
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    for row in self.c.fetchall():
        grpmbrs += "UID:"+str(row[0])+"\r\n"
    grpmbrs += "\r\n"
    self.sendString(grpmbrs)
    
# This function implements the SENDMSG [UID] "[message]" command
def sendMsgHandle(self, request, connections):
    print("sendMsgHandle")
    split = request.split("\r\n")
    print(split)
    sid = split[1].lstrip("SID:")
    gid = split[2].lstrip("GID:")
    message = split[3]
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    targetusers = []
    for row in self.c.fetchall():
        targetusers.append(row[0])
        
    self.c.execute("SELECT userid, status FROM users")
    for row in self.c.fetchall():
        if row[0] in targetusers:
            if row[1] == 1:
                for user in connections:
                    if user.ID == row[0] and user.ID != self.ID:
                        user.deliverMsg(gid, user.ID, message)
            else:
                if not row[0] == self.ID:
                    self.storeMsg(row[0], gid, message)
        
    """for user in connections:
        if user.ID in targetusers and self.ID != user.ID:
            if user.online = True:
                user.sendString(message)
            else:
                user.storeMsg(user.IDgid, message)"""
    
    self.sendString("MSG OK\r\n")
    
    

