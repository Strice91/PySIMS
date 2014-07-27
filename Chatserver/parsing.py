import uuid
import time
import hashlib

# This function implements the REGISTER [username] [password] command
def registerHandle(self, request):
    print("registerHandle")
    split = request.split("\r\n")
    username = split[0].split(' ')[1].strip()
    password = split[0].split(' ')[2].strip()
    question = split[1]
    answer = split[2]
    passhash = hashlib.md5()
    passhash.update(password.encode('UTF-8'))
    # Check if username already in DB
    self.c.execute("SELECT username FROM users WHERE username=?", (username,))
    if not self.c.fetchall() == []:
        self.sendString("REGUSER ERR\r\n")
    else:
        # If username is free add the user to the database
        self.c.execute("INSERT INTO users (username, password, question, answer) VALUES (?,?,?,?)", (username, passhash.hexdigest(), question, answer))
        self.db.commit()
        print("Successfully registered user",username)
        self.sendString("REGISTER OK\r\n")
    return True

# This function implements the USER [username] and PASS [password] command
def userHandle(userobject, request, users):
    print("userHandle")
    # print(request)
    split = request.split(" ")
    # Get username from request
    username = split[1].strip()
    # Check if user in DB
    userobject.c.execute("SELECT * FROM users WHERE username=?", (username,))
    login = userobject.c.fetchone()
    if login == None:
        userobject.sendString("USER ERR\r\n")
        print("User", username, "not found.")
        return True
    else:
        userobject.sendString("USER OK\r\n")
        # Wait for PASS [password] command
        passcommand = userobject.getString()
        # print(passcommand)
        if not "PASS" in passcommand:
            userobject.sendString("LOGIN ABORTED\r\n")
            return True
        else:
            # Check if received password is ok
            password = passcommand.split(" ")[1].strip()
            passhash = hashlib.md5()
            passhash.update(password.encode('UTF-8'))
            if not passhash.hexdigest() == login[2]:
                userobject.sendString("PASS ERR\r\n")
                print("User", username, "entered wrong password.")
                return True
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
                userobject.updateUserLists()
    return True

# This function implements the GETLIST command
def getListHandle(self):
    print("getListHandle")
    self.sendList([self])

# This function implements the PULLMSGS command
def pullMsgsHandle(self):
    print("pullMsgsHandle")
    self.pushMsgs()

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
    # Convert all UIDs to ints
    intuserids = []
    for userid in userids:
        intuserids.append(int(userid))
    # Check if there is already a group with this constellation
    gid = checkForExistingGroup(self, intuserids)
    # if not, create a new one
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
    # Else return the known GID
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
    # print(request.split("\r\n"))
    gid = request.split("\r\n")[1].lstrip("GID:")
    grpmbrs = "MEMBERS\r\n"
    grpmbrs += "GID:"+gid+"\r\n"
    # Get group members from DB
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    for row in self.c.fetchall():
        grpmbrs += "UID:"+str(row[0])+"\r\n"
    grpmbrs += "\r\n"
    self.sendString(grpmbrs)

# This function implements the UPDATEGROUP command
def updateGrpHandle(self, request, connections):
    print("updateGrpHandle")
    split = request.split('\r\n')
    gid = split[1].lstrip('GID:')
    # Delete all current group members
    self.c.execute("DELETE FROM groupmembers WHERE GID=?", (gid,))
    uids = []
    # Add the new users to the group
    for member in split[2:]:
        if not member == split[-1]:
            userline = member.split(',')
            # print(userline)
            uid = int(userline[0].lstrip('UID:'))
            flag = userline[1].strip()  
            if flag == "1":
                uids.append(uid)
                self.c.execute("INSERT INTO groupmembers (GID, UID) VALUES (?, ?)", (gid, uid))
    self.db.commit()
    self.sendString("UPDATEGROUP "+gid+" OK\r\n")
    msg = "MEMBERS\r\n"
    msg += "GID:"+gid+"\r\n"
    for uid in uids:
        msg += "UID:"+str(uid)+"\r\n"
    msg += "\r\n"
    # Send the new group to every user which is online and part of the new group
    for user in connections:
        if user.ID in uids and user.online == True:
            print("Send new group to user", user.ID)
            user.sendString(msg)
    
# This function implements the SENDMSG [UID] "[message]" command
def sendMsgHandle(self, request, connections):
    print("sendMsgHandle")
    split = request.split("\r\n")
    sid = split[1].lstrip("SID:")
    gid = split[2].lstrip("GID:")
    message = split[3]
    # print(message)
    # Get target group members
    self.c.execute("SELECT uid FROM groupmembers WHERE gid=?", (gid,))
    targetusers = []
    for row in self.c.fetchall():
        targetusers.append(row[0])
    
    self.c.execute("SELECT userid, status FROM users")
    # Deliver the message to every user in the target group
    for row in self.c.fetchall():
        if row['userid'] in targetusers:
            if row['status'] == "1":
                for user in connections:
                    if user.ID == row[0] and user.ID != self.ID:
                        user.deliverMsg(gid, self.ID, message)
            else:
                # if user is not online, store the message
                if not row['userid'] == self.ID:
                    self.storeMsg(self.ID, row[0], gid, message)
    
    # Return the MSG OK to the sender
    self.sendString("MSG OK\r\nGID:"+gid+"\r\n\r\n")

# Checks if there is already a group of users with "userids" as members
def checkForExistingGroup(self, userids):
    # print(userids)
    self.c.execute("SELECT GID, UID FROM groupmembers")
    guids = {}
    for row in self.c.fetchall():
        if not row['GID'] in guids:
            guids[row['GID']] = []

    self.c.execute("SELECT GID, UID FROM groupmembers")
    for row in self.c.fetchall():
        guids[row['GID']].append(row['UID'])

    userids.sort()

    for group in guids.keys():
        guids[group].sort()
        if userids == guids[group]:
            return group

    return None

# This function implements the FORGOTPASS process
def forgotPassHandle(self, request):
    print('forgotPassHandle')
    user = request.split(' ')[1].strip()
    print("User", user, "forgot password")
    # Get security question from DB
    self.c.execute("SELECT question, answer FROM users WHERE username=?", (user,))
    row = self.c.fetchone()
    # Check if user exists
    if row:
        # if user exists, send security question
        msg = "FORGOTPASS OK\r\n"
        msg += row['question']+"\r\n"
        msg += "\r\n"
        self.sendString(msg)
        print("User found")
    else:
        self.sendString("FORGOTPASS ERR\r\n")
        return
    # Wait for the answer of the user
    useranswer = self.getString().strip()
    useranswer = useranswer.split(' ')[1]
    print(useranswer)
    # Check if answer is correct
    if useranswer == row['answer']:
        print("User sent correct answer")
        self.sendString("ANSWER OK\r\n")
    else:
        self.sendString("ANSWER ERR\r\n")
        return
    # Wait for new password
    userpass = self.getString()
    userpass = userpass.split(' ')[1].strip()
    # Hash password and replace old one in DB
    passhash = hashlib.md5()
    passhash.update(userpass.encode('UTF-8'))
    self.c.execute("UPDATE users SET password=? WHERE username=?", (passhash.hexdigest(), user))
    self.db.commit()
    self.sendString("CHANGEPASS OK\r\n")
    print("changepass successful")
