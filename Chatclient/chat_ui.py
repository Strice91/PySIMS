import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from os import path
from TextTools import TextTools
import chatControl


class QChatWindow(QWidget):

    def __init__(self, gid, senderID=None, msg=None, parent=None):
        super(QChatWindow, self).__init__()

        self.parent = parent
        self.tcp = parent.tcp
        self.tcp.recvAns.connect(self.parseAns)
        self.contact = {'UID':'10','name':'test','status':'online'}
        self.GID = gid
        self.SID = parent.parent.SID
        self.UID = parent.UID
        self.members = []
        self.initUI()

        if msg:
            self.appendText(senderID,msg)

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
        self.SendBtn.setShortcut('Ctrl+Return')
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

        self.showChatContainer = QWidget()

        ContainerLayout = QVBoxLayout()

        self.showChat = QTextBrowser()
        #self.showChat.setStyleSheet("background: rgb(255,255,255); color: black")
        self.showChat.setMinimumSize(359,20)

        policy = self.showChat.sizePolicy()
        policy.setHorizontalStretch(1)
        self.setSizePolicy(policy)

        ContainerLayout.addLayout(self.MemberControl)
        ContainerLayout.addWidget(self.showChat)

        self.showChatContainer.setLayout(ContainerLayout)

    def initMemberControl(self):
        self.MemberControl = QHBoxLayout()

        self.MemberBtn = QPushButton()
        self.MemberBtn.setIcon(QIcon('img/chat/group.png'))
        self.MemberBtn.setToolTip('Mitglieder des Chats auswaehlen')
        self.MemberBtn.clicked.connect(self.openAddWindow)

        #self.RemoveUserBt = QPushButton()
        #self.RemoveUserBt.setIcon(QIcon('img/chat/rem.png'))

        self.MemberControl.addWidget(self.MemberBtn)
        #self.MemberControl.addWidget(self.RemoveUserBt)
        self.MemberControl.addStretch(1)

    def initUI(self):

        self.requestMembers()

        # Adjust Window ----------------------------------------------
        self.resize(400, 300)
        self.setWindowTitle('GID: ' + self.GID)
        StatusImgPath = path.join('img/user/',self.contact['status'] +'.png')
        self.setWindowIcon(QIcon(StatusImgPath)) 

        self.initMemberControl()
        self.initEditForm()
        self.initShowChat()
        
        # Build Main Layout
        layout = QHBoxLayout(self)
        # Splitter Layout
        splitter = QSplitter(Qt.Vertical)
        splitter.setSizes([300,50])

        #splitter.addLayout(self.Control)
        splitter.addWidget(self.showChatContainer)
        splitter.addWidget(self.editFormContainer)
        # Add Splitter to Main Layout
        layout.addWidget(splitter)
        self.setLayout(layout)
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.SendBtn.clicked.connect(self.sendMsg)
        

    def appendText(self, senderID, text, sendtime=None):

        if not sendtime:
            sendtime = time.time()

        #print('MSG from ID:', senderID)
        #print('Time:', sendtime)
        #for user in self.parent.contactList:
            #print (user)

        if senderID in self.parent.contactList and senderID != self.UID:
            senderName = self.parent.contactList[senderID]['name']
        elif senderID == self.UID:
            senderName = 'Ich'
        else:
            senderName = 'Unbekannt'

        self.showChat.append(TextTools.newMsg(senderName,text,sendtime))
        

    def sendMsg(self):
        
        text = self.TextEdit.toPlainText()

        if text:
            req = 'SENDMSG\r\n'
            req += 'SID:' + self.SID + '\r\n'
            req += 'GID:' + self.GID + '\r\n'
            req += text + '\r\n\r\n'
            self.tcp.sendReq(req)

            self.appendText(self.UID,text)

    def sendAck(self):
        #self.tcp.sendReq('ACK\r\n')
        #print('ACK sent')
        pass

    def requestMembers(self):
        req = "GETGRPMBRS\r\n"
        req += "GID:"
        req += self.GID
        req += "\r\n\r\n"
        self.tcp.sendReq(req)

    def updateMembers(self, memberList):
        self.members = memberList
        title = "Chat mit: "
        for uid in memberList:
            if not uid == self.UID:
                title += self.parent.contactList[uid]['name'] + " "
        self.setWindowTitle(title)

    def lostCon(self):
        print('Hilfe')

    @Slot(str, str)
    def newMsg(self, senderID, msg):
        pass

    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):
        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            print('------  Chat Window Recived: -----')
            print(ans)
            print('----------------------------------')

            if ans[0] == 'DLVMSG':
                GID = ans[1].split(':')
                UID = ans[2].split(':')
                msg = ans[3]
                #print('GID:', GID)
                #print('UID:', UID)
                if GID[0] == 'GID':
                    if GID[1] == self.GID:
                        if UID[0] == 'UID':
                            senderID = UID[1]
                            print('Display new Message')
                            self.appendText(senderID,msg)
                            self.sendAck()

            elif ans[0] == 'MEMBERS':
                GID = ans[1].split(':')
                if GID[0] == 'GID' and GID[1] == self.GID:

                    members = []
                    for member in ans[1:]:
                        if member:
                            m = member.split(':')
                            if m[0] == 'UID':
                                members.append(m[1])
                    print('Updating Userlist')
                    self.updateMembers(members)

            elif ans[0] == 'MSG OK':
                GID = ans[1].split(':')
                if GID[0] == 'GID' and GID[1] == self.GID: 
                    print('Message delivered')
                    self.TextEdit.setText('')

    def openAddWindow(self):
        self.addWindow = chatControl.chatAddWindow(parent = self)
        self.addWindow.show()

    def closeEvent(self, ev):
        del self.parent.ChatWindows[self.GID]
        try:
            self.addWindow.close()
        except:
            pass
        finally:
            print('Chat closed!')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    contact = {'UID': 'c5355ed9cba4481aa49409b4a15cbd77', 'name': 'Hans', 'status': 'online'}
    ChatW = QChatWindow(contact)
    ChatW.show()
    sys.exit(app.exec_())