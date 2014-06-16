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
        
    def initUI(self):
        
        self.okButton = QtGui.QPushButton("OK")
        self.cancelButton = QtGui.QPushButton("Cancel")

        self.okButton.clicked.connect(self.send)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)

        vbox = QtGui.QVBoxLayout()
        self.text = QtGui.QTextBrowser()
        self.edit = QtGui.QLineEdit()
        vbox.addWidget(self.text)
        vbox.addWidget(self.edit)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()

    def send(self):
        msg = self.edit.text() 
        self.tcp.sendReq(msg)

    @QtCore.Slot(str)
    def printAns(self, lastReq, ans):
        print('Ans:', ans)
        self.text.append('Server: |' + ans + '|')
        print(ans.split())

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()