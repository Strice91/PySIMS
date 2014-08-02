# Code from http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?index=415&key=QTcpSocketConnectToSMTP

from PySide.QtGui import * 
from PySide.QtCore import * 
from PySide.QtNetwork import * 
import sys
import time

class TcpClient(QTcpSocket): 
  
    recvAns = Signal(str, str) 
    ConError = Signal(str)

    def __init__(self, ip, port, parent=None):
        super(TcpClient, self).__init__(parent)

        if not ip:
            # Select Default IP
            #self.ip = '129.187.223.104' # LKN Server
            #self.ip = 'localhost' # Local Host
            #self.ip = '10.180.15.89' # Other Host
            self.ip = '192.168.2.114' # Other Host
        else:
            self.ip = ip

        if not port:
            # Select Default Port
            self.port = 8075
        else:
            self.port = port

        print('IP:', self.ip)
        print('PORT:', self.port)
        # Connect to the Chatserver
        self.con()

        # Connect the ReadyRead Signal to the Read Function
        self.readyRead.connect(self.slotReadData)
        self.error.connect(self.connectionError)
        self.ans = ""
        self.lastReq = ""
    
    def con(self):
        self.connectToHost(self.ip,self.port)
        #print(self.conncted())

    @Slot()
    def slotReadData(self):
        # Read the incoming Data
        self.ans = str(self.readAll())

        # Print the recived Data
        print('##########  Server says ##########')
        print(self.ans)
        print('##################################')

        # Send Signal to the Windows
        self.recvAns.emit(self.lastReq, self.ans)
    
    @Slot()
    def sendReq(self, msg):
        # Send Data to the Server
        self.write(msg)
        self.lastReq = msg
        # Print the Sent Data
        print('###########  Send MSG ############')
        print (msg) 
        print('##################################') 

    @Slot()
    def connectionError(self, err):
        if err is QAbstractSocket.RemoteHostClosedError:
            self.ConError.emit('ConnectionClosed')
        elif err is QAbstractSocket.ConnectionRefusedError:
            self.ConError.emit('ConnectionRefused')
        elif err is QAbstractSocket.HostNotFoundError:
            self.ConError.emit('HostNotFound')
        else:
            self.ConError.emit('UnknownNetworkError')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    client = MyTCPClient('localhost',8075)

    app.exec_()
    client = MyTCPClient('localhost',8075)

    client.sendMessage('USER stefan')
    print('Ans:', client.ans)
