from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *

class chatAddWindow(QDialog):

    def __init__(self, parent=None):
        super(chatAddWindow, self).__init__()

        self.parent = parent
        self.contactList = parent.parent.contactList
        self.members = parent.members
        self.tcp = parent.tcp
        self.GID = parent.GID

        self.initUI()

    def initUI(self):

        # Adjust Window ----------------------------------------------
        self.resize(150, 300)
        self.setWindowTitle('GID: ' + self.GID)
        
        layout = QVBoxLayout()

        text = QLabel('Mitglieder auswaehlen:')

        self.Btn = QPushButton('Aendern')
        self.Btn.clicked.connect(self.updateMembers)

        ContactScroll = QScrollArea()
        ContactScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        ContactScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ContactScroll.setWidgetResizable(False)
        ContactScroll.setMinimumSize(30,200)

        ContactScrollContainer = QWidget()
        
        ContactListLayout = QVBoxLayout()

        self.CheckBoxList = {}

        for uid in self.contactList:

            contact = self.contactList[uid]

            cLayout = QHBoxLayout()
            cLabel = QLabel(contact['name'])

            cCheck = QCheckBox()
            if uid in self.members:
                cCheck.setCheckState(Qt.Checked)

            self.CheckBoxList[uid] = cCheck

            cLayout.addWidget(cLabel)
            cLayout.addStretch(1)
            cLayout.addWidget(cCheck)

            ContactListLayout.addLayout(cLayout)

        ContactScrollContainer.setLayout(ContactListLayout)

        ContactScroll.setWidget(ContactScrollContainer)

        layout.addWidget(text)
        layout.addWidget(ContactScroll)
        layout.addWidget(self.Btn)

        self.setLayout(layout)

    def updateMembers(self):

        statusList = []
        statusList.append('UID:'+ self.parent.UID + ",1")
        for uid in self.CheckBoxList:
            status = self.CheckBoxList[uid].isChecked()
            statusStatement = "UID:" + uid
            if status:
                statusStatement += ",1"
            else:
                statusStatement += ",0"

            statusList.append(statusStatement)
        #print(statusList)
        self.sendMemberList(statusList)

    def sendMemberList(self, statusList):
        req = "UPDATEGROUP\r\n"
        req += "GID:" + self.GID + "\r\n"
        req += '\r\n'.join(statusList)
        req += '\r\n'

        self.tcp.sendReq(req)


        