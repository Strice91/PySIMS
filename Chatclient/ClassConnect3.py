# Code from http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?index=415&key=QTcpSocketConnectToSMTP

from PySide.QtGui import * 
from PySide.QtCore import * 
from PySide.QtNetwork import * 
import sys
import time

class MyTCPClient(QTcpSocket): 
  
    sendAns = Signal(str) 

    def __init__(self, ip, port, parent=None):
        super(MyTCPClient, self).__init__(parent)

        # Connect to the Chatserver
        self.connectToHost(ip,port)
        # Connect the ReadyRead Signal to the Read Function
        self.readyRead.connect(self.slotReadData)
        self.ans = ""
 

    @Slot()
    def slotReadData(self):
        # Read the incoming Data
        self.ans = self.readAll()
        print ("Server says: ", self.ans)
    
    @Slot()
    def sendMessage(self, msg):
        # Send Data to the Server
        self.write(msg)
        print ('Sent Message: ', msg)  


def main():  
    app = QApplication(sys.argv)
    # Crearte new TCP Object
    client = MyTCPClient("localhost",8075)

    #timer = QTimer()
    #client.connectToHost("localhost",8075)
    #client.sendMessage('USER stefan')
    #timer.singleShot(3,client,SLOT("sendMessage()"))
    #QObject.connect(client,SIGNAL("readyRead()"),client,SLOT("slotReadData()"))    
    #QObject.connect(timer,SIGNAL("timeout()"),client,SLOT("sendMessage()"))    

    client.sendMessage('USER stefan')
    #client.sendMessage('PASS badbad')

    #------------------------
    # Process Answer here:
    #------------------------

    print('Ans: ', client.ans)
           
    return app.exec_()
if __name__ == '__main__':
  main()   