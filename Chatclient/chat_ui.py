import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from os import path
import TextTools


class QChatWindow(QWidget):

    def __init__(self, gid, parent=None):
        super(QChatWindow, self).__init__()

        self.parent = parent
        self.tcp = parent.tcp
        self.tcp.recvAns.connect(self.parseAns)
        self.contact = {'UID':'10','name':'test','status':'online'}
        self.GID = gid
        self.SID = parent.parent.SID
        self.UID = parent.UID
        self.initUI()

    def initEditForm(self):
        
        self.editFormContainer = QWidget()

        # Layout for the Edit Form
        self.editForm = QHBoxLayout()

        # Create Control Section
        controlSect = QVBoxLayout()

        # Text Field
        self.TextEdit = QTextEdit()
        self.TextEdit.setMaximumSize(390,70)

        # Send Buttoen
        self.SendBtn = QPushButton()
        self.SendBtn.setIcon(QIcon('img/chat/send.png'))
        self.SendBtn.setShortcut('Return')
        #self.SendBtn.setIconSize(QSize(20,20))

        # Emoticons Button
        self.EmotBtn = QPushButton()
        self.EmotBtn.setIcon(QIcon('img/chat/emot.png'))
        #self.EmotBtn.setIconSize(QSize(20,20))

        # Add Widget to Control Section
        controlSect.addWidget(self.SendBtn)
        controlSect.addWidget(self.EmotBtn)
        controlSect.addStretch(1)

        # Add Widgets to Main Form
        self.editForm.addWidget(self.TextEdit)
        self.editForm.addLayout(controlSect)

        # Add the Main Form to Container Widget
        self.editFormContainer.setLayout(self.editForm)

    def initShowChat(self):

        self.showChat = QTextBrowser()
        #self.showChat.setStyleSheet("background: rgb(255,255,255); color: black")
        self.showChat.setMinimumSize(359,20)

        policy = self.showChat.sizePolicy()
        policy.setHorizontalStretch(1)
        self.setSizePolicy(policy)

    def initUI(self):

        # Adjust Window ----------------------------------------------
        self.resize(400, 300)
        self.setWindowTitle('Chat mit ' + self.contact['name'])
        StatusImgPath = path.join('img/user/',self.contact['status'] +'.png')
        self.setWindowIcon(QIcon(StatusImgPath)) 

        self.initEditForm()
        self.initShowChat()

        # Build Main Layout
        layout = QHBoxLayout(self)
        # Splitter Layout
        splitter = QSplitter(Qt.Vertical)
        splitter.setSizes([300,50])

        splitter.addWidget(self.showChat)
        splitter.addWidget(self.editFormContainer)
        # Add Splitter to Main Layout
        layout.addWidget(splitter)
        self.setLayout(layout)
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.SendBtn.clicked.connect(self.sendMsg)

    def appendText(self, userName, text, time=time.time()):
        self.showChat.append(TextTools.TextTools.newMsg(userName,text,time))

    def sendMsg(self):
        
        text = self.TextEdit.toPlainText()
        userName = 'Ich'

        if text:
            req = 'SENDMSG\r\n'
            req += 'SID:' + self.SID + '\r\n'
            req += 'GID:' + self.GID + '\r\n'
            req += text + '\r\n\r\n'
            print(req)
            self.tcp.sendReq(req)

            #self.appendText(userName,text)

    def parseAns(self):
        pass





if __name__ == '__main__':

    app = QApplication(sys.argv)
    contact = {'UID': 'c5355ed9cba4481aa49409b4a15cbd77', 'name': 'Hans', 'status': 'online'}
    ChatW = QChatWindow(contact)
    ChatW.show()
    sys.exit(app.exec_())