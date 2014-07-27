#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

In this example, we position two push
buttons in the bottom-right corner 
of the window. 

author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys
from PySide import QtGui
from PySide import QtCore
from ClassConnect import TcpClient

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.tcp = TcpClient('localhost',8075)
        self.tcp.recvAns.connect(self.printAns)
        self.initUI()
        self.SID = None
        
    def initUI(self):

        

        vbox = QtGui.QVBoxLayout()

        self.text = QtGui.QTextBrowser()
        self.user = QtGui.QPushButton("USER")
        self.passwd = QtGui.QPushButton("PASS")
        self.grp = QtGui.QPushButton("GROUP")
        self.mkgrp = QtGui.QPushButton("MAKEGROUP")
        self.getgrpmbrs = QtGui.QPushButton("GETGRPMBRS")

        vbox.addWidget(self.text)
        vbox.addWidget(self.user)
        vbox.addWidget(self.passwd)
        vbox.addWidget(self.grp)
        vbox.addWidget(self.mkgrp)
        vbox.addWidget(self.getgrpmbrs)

        self.user.clicked.connect(self.sendUSER)
        self.passwd.clicked.connect(self.sendPASS)
        self.grp.clicked.connect(self.sendGRP)
        self.mkgrp.clicked.connect(self.sendMKGRP)
        self.getgrpmbrs.clicked.connect(self.sendGETGRPMBRS)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()

    def sendUSER(self):
        msg = "USER test"
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)

    def sendPASS(self):
        msg = "PASS test"
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)

    def sendGRP(self):
        msg = "GETGRPS\r\nSID:" + self.SID + "\r\n\r\n" 
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)

    def sendMKGRP(self):
        msg = "MKGRP\r\nUID:10,11\r\nSID:" + self.SID + "\r\n\r\n" 
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)

    def sendGETGRPMBRS(self):
        msg = "GETGRPMBRS\r\nGID:10\r\n\r\n" 
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)

    """def sendMemb(self):
        msg = "GETGRPS\r\nSID:" + self.SID + "\r\n\r\n" 
        self.tcp.sendReq(msg)
        print ('MSG: ', msg)"""

    @QtCore.Slot(str)
    def printAns(self, lastReq, ans):
        print('Ans:', ans)
        self.text.append('Server: |' + ans + '|')
        myAns = ans.split()
        print(myAns)
        if myAns[0] == 'PASS':
            SID = myAns[2].split(':')
            self.SID = SID[1]

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()