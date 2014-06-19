# Code from http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?index=415&key=QTcpSocketConnectToSMTP

from PySide.QtGui import * 
from PySide.QtCore import * 
from PySide.QtNetwork import * 
import sys
import time

class TcpClient(QTcpSocket): 
  
    recvAns = Signal(str, str) 

    def __init__(self, ip='localhost', port=8075, parent=None):
        super(TcpClient, self).__init__(parent)

        # Connect to the Chatserver
        self.ip = '129.187.223.104' # LKN Server
        #self.ip = 'localhost' # Other Host
        self.port = 8075
        self.con()

        # Connect the ReadyRead Signal to the Read Function
        self.readyRead.connect(self.slotReadData)
        self.ans = ""
        self.lastReq = ""
    
    def con(self):
        self.connectToHost(self.ip,self.port)
        #print(self.conncted())

    @Slot()
    def slotReadData(self):
        # Read the incoming Data
        self.ans = str(self.readAll())
        print ("Req: ", self.lastReq, "Ans: ", self.ans)
        self.recvAns.emit(self.lastReq, self.ans)
        #self.lastReq = ""
    
    @Slot()
    def sendReq(self, msg):
        # Send Data to the Server
        self.write(msg)
        self.lastReq = msg
        #print ('Sent Message: ', msg)  


if __name__ == '__main__':

    app = QApplication(sys.argv)
    client = MyTCPClient('localhost',8075)

    app.exec_()
    client = MyTCPClient('localhost',8075)

    client.sendMessage('USER stefan')
    print('Ans:', client.ans)