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
        self.sendString("ERRUSER\r\n")
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
                self.sendString("PASS WRONG\r\n")
            else:
                # If password is ok, set the UID, generate SID, set User to 'online' and return OK and SID
                self.ID = login[0]
                for user in connections:
                    if user.online == True and user.ID == self.ID:
                        user.sendString("CLOSING CONNECTION\r\n")
                        user.request.close()
                self.SID = uuid.uuid4().hex
                self.setOnline(True)
                self.sendString("PASS OK\r\n")
                self.sendString("SID:"+str(self.SID)+"\r\n\r\n")
    return True

# This function implements the GETLIST command
def getListHandle(self, request):
    print("getListHandle")
    self.sendString('LIST\r\n')
    # Generate list of users, select only coloums 'userid','username' and 'status'
    self.c.execute("SELECT userid, username, status FROM users")
    # For each user send userid, username and status
    for row in self.c.fetchall():
        self.sendString("UID:"+str(row[0])+","+row[1]+","+row[2]+"\r\n")
    # Terminate list
    self.sendString("\r\n")

# This function implements the MKGRP command
def mkgrpHandle(self):
    print("mkgrpHandle")
    userids = self.getString()
    userids = userids.lstrip("UID:").rstrip("\r\n")
    userids = userids.split(',')
    sid = self.getString()
    sid = sid.lstrip("SID:").rstrip("\r\n")
    self.getString()
    timestamp = int(time.time())
    self.c.execute("INSERT INTO groups (creationdate) VALUES (?)", (timestamp,))
    self.c.execute("SELECT last_insert_rowid()")
    gid = self.c.fetchone()[0]
    for uid in userids:
        self.c.execute("INSERT INTO groupmembers (GID, UID) VALUES (?, ?)", (gid, uid))
    self.db.commit()
    self.sendString("MKGRP OK\r\n")
    
def getgrpsHandle(self):
    print("getgrpsHandle")
    sid = self.getString().lstrip("SID:").rstrip("\r\n")
    self.getString()
    self.sendString("GRPS\r\n")
    self.c.execute("SELECT gid FROM groupmembers WHERE UID=?", (self.ID,))
    for row in self.c.fetchall():
        self.sendString("GID:"+str(row[0])+"\r\n")
    self.sendString("\r\n")

def getgrpmbrsHandle(self):
    gid = self.getString().lstrip("GID:").rstrip("\r\n")
    self.sendString("MEMBERS\r\n")
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    for row in self.c.fetchall():
        self.sendString("UID:"+str(row[0])+"\r\n")
    self.sendString("\r\n")
    
# This function implements the SENDMSG [UID] "[message]" command
def sendMsgHandle(self, request, connections):
    sid = self.getString().lstrip("SID:").rstrip("\r\n")
    gid = self.getString().lstrip("GID:").rstrip("\r\n")
    message = self.getString()
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    targetusers = []
    for row in self.c.fetchall():
        targetusers.append(row[0])
    for user in connections:
        if user.ID in targetusers and self.ID != user.ID:
            user.sendString(message)
    self.sendString("MSG OK\r\n")
    
    

