import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
import TextTools


class QChatWindow(QWidget):

    def __init__(self, contact):
        super(QChatWindow, self).__init__()

        self.contact = contact
        self.initUI()

    def initEditForm(self):
        
        self.editFormContainer = QWidget()

        # Layout for the Edit Form
        self.editForm = QHBoxLayout()

        controlSect = QVBoxLayout()

        # Text Field
        self.TextEdit = QTextEdit()

        # Send Buttoen
        self.SendBtn = QPushButton()
        self.SendBtn.setIcon(QIcon('img/chat/send.png'))

        # Emoticons Button
        self.EmotBtn = QPushButton()
        self.EmotBtn.setIcon(QIcon('img/chat/emot.png'))

        controlSect.addWidget(self.SendBtn)
        controlSect.addWidget(self.EmotBtn)
        controlSect.addStretch(1)

        self.editForm.addWidget(self.TextEdit)
        self.editForm.addLayout(controlSect)

        self.editFormContainer.setLayout(self.editForm)

    def initShowChat(self):

        self.showChat = QTextEdit('------------ Session Beginn: heute ------------')
        self.showChat.setEnabled(False)
        self.showChat.setStyleSheet("background: rgb(255,255,255); color: black")


    def initUI(self):

        # Adjust Window ----------------------------------------------
        self.resize(400, 300)
        self.setWindowTitle('Chat mit ' + self.contact['name'])

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
            self.appendText(userName,text)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    contact = {'UID': 'c5355ed9cba4481aa49409b4a15cbd77', 'name': 'Hans', 'status': 'online'}
    ChatW = QChatWindow(contact)
    ChatW.show()
    sys.exit(app.exec_())