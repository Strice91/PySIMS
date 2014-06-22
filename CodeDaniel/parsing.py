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
        self.sendString("REGUSER ERR\r\n")
    else:
        # If username is free add the user to the database
        self.c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, passhash.hexdigest()))
        self.db.commit()
        print("Successfully registered user",username)
        self.sendString("REGISTER OK\r\n")
    return True

# This function implements the USER [username] and PASS [password] command
def userHandle(userobject, request, users):
    print("userHandle")
    if "WEBUI" in request:
        # print("WebUI")
        userobject.WebUI = True
    split = request.split(" ")
    # Get username from request
    username = split[1].strip()
    # Check if user in DB
    userobject.c.execute("SELECT * FROM users WHERE username=?", (username,))
    login = userobject.c.fetchone()
    if False:#login == None:
        userobject.sendString("USER ERR\r\n")
        print("User", username, "not found.")
    else:
        userobject.sendString("USER OK\r\n")
        # Wait for PASS [password] command
        passcommand = userobject.getString()
        if not "PASS" in passcommand:
            userobject.sendString("LOGIN ABORTED\r\n")
        else:
            # Check if received password is ok
            password = passcommand.split(" ")[1].strip()
            passhash = hashlib.md5()
            passhash.update(password.encode('UTF-8'))
            if not passhash.hexdigest() == login[2]:
                userobject.sendString("PASS ERR\r\n")
                print("User", username, "entered wrong password.")
            else:
                # If password is ok, set the UID, generate SID, set User to 'online' and return OK and SID
                userobject.ID = login[0]
                for user in users:
                    if user.online == True and user.ID == userobject.ID:
                        user.sendString("CLOSING CONNECTION\r\n")
                        user.request.close()
                        print("Closed connection of user", username, "because of multiple login.")
                userobject.SID = uuid.uuid4().hex
                userobject.setOnline(True)
                userobject.sendString("PASS OK\r\nUID:"+str(userobject.ID)+"\r\nSID:"+str(userobject.SID)+"\r\n\r\n")
                userobject.c.execute("UPDATE users SET SID=? WHERE userid=?", (userobject.SID, userobject.ID))
                userobject.db.commit()
                print("User "+username+" logged in.")
                userobject.pushMsgs()
                userobject.updateUserLists()
    return True

# This function implements the GETLIST command
def getListHandle(self):
    print("getListHandle")
    self.sendList([self])

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
    intuserids = []
    for userid in userids:
        intuserids.append(int(userid))
    gid = checkForExistingGroup(self, intuserids)
    if gid == None:
        timestamp = int(time.time())
        self.c.execute("INSERT INTO groups (creationdate) VALUES (?)", (timestamp,))
        self.c.execute("SELECT last_insert_rowid()")
        gid = self.c.fetchone()[0]
        for uid in userids:
            self.c.execute("INSERT INTO groupmembers (GID, UID) VALUES (?, ?)", (gid, uid))
        self.db.commit()
        self.sendString("MKGRP OK\r\nGID:"+str(gid)+"\r\n\r\n")
        print("Created group", gid, "with users", userids)
    else:
        self.sendString("MKGRP OK\r\nGID:"+str(gid)+"\r\n\r\n")
        # print("Group alread exists")

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

def addToGrpHandle(self, request):
    print("addToGrpHandle")
    split = request.split('\r\n')
    
# This function implements the SENDMSG [UID] "[message]" command
def sendMsgHandle(self, request, connections):
    print("sendMsgHandle")
    split = request.split("\r\n")
    sid = split[1].lstrip("SID:")
    gid = split[2].lstrip("GID:")
    message = split[3]
    print(message)
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    targetusers = []
    for row in self.c.fetchall():
        targetusers.append(row[0])
        
    self.c.execute("SELECT userid, status FROM users")
    for row in self.c.fetchall():
        if row[0] in targetusers:
            if row[1] == "1":
                print("User online, deliver Message directly")
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

def checkForExistingGroup(self, userids):
    self.c.execute("SELECT GID, UID FROM groupmembers")
    guids = {}
    for row in self.c.fetchall():
        if not row['GID'] in guids:
            guids[row['GID']] = []

    self.c.execute("SELECT GID, UID FROM groupmembers")
    for key in guids.keys():
        for row in self.c.fetchall():
            if row['GID'] == key:
                guids[key].append(row['UID'])

    # print(guids)

    for group in guids.keys():
        #print(group)
        # print(userids)
        # print(guids[group])
        if userids == guids[group]:
            return group

    return None

    
    

