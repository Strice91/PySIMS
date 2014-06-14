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
        # Coonect the ReadyRead Signal to the Read Function
        #self.readyRead.connect(self.slotReadData)
        self.ans = ""
 

    @Slot()
    def slotReadData(self):
        print ("Server says:\n")
        ans = self.readAll()
        print (ans)
    
    @Slot()
    def sendMessage(self, msg):
        self.write(msg)
        print (msg)  

    @Slot(str)
    def returnData(self, ans):
        return ans



def main():  
    app = QApplication(sys.argv)
    client = MyTCPClient("localhost",8075)
    timer = QTimer()
    #client.connectToHost("localhost",8075)
    #client.sendMessage('USER stefan')
    print(client.ans)
    #timer.singleShot(3,client,SLOT("sendMessage()"))
    #QObject.connect(client,SIGNAL("readyRead()"),client,SLOT("slotReadData()"))    
    #QObject.connect(timer,SIGNAL("timeout()"),client,SLOT("sendMessage()"))    

    client.sendMessage('USER stefan')
    
    client.slotReadData()

           
    return app.exec_()
if __name__ == '__main__':
  main()   