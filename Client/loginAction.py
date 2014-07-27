
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
 
class LoginAction(QWidget):
   
    def __init__(self, parent=None):
        super(LoginAction, self).__init__(parent)

    # Login User
    def loginUser(self):
        print('Log mich ein!')
        #self.usernameEdit.insert('HAllo')
        user = self.usernameEdit.text()
        msg = 'USER ' + user;
        self.tcp.sendMessage(msg)

    def login(self):
        self.usernameEdit.insert('HAllo')

    def requestPass(self):
    	print ("Der Depp hat sein Passwort vergessen!")

    def abbortLogin(self):
    	print ("Halt nicht einloggen")

    def registerUser(self):
    	print ("Hey, ein neuer User")

    @Slot(str, str)
    def parseAns(self, lastReq, ans):
        print ('LastReq: ', lastReq, ' Ans: ', ans)
        self.login()
        
       