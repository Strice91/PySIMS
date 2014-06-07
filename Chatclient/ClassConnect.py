
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *

class Connect(QTcpSocket):
    def __init__(self, parent=None):
        super(Connect, self).__init__(parent)
        self.PORT = 8075
        self.IP = '192.168.178.18'

    def connectToServer(self):
    	self.connectToHost(self.IP,self.PORT)

if __name__ == '__main__':
	c = Connect()
	c.connectToServer()
	c.write('USER test')
	input()