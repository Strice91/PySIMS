from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *

class chatEditWindow(QDialog):

    def __init__(self, parent=None):
        super(chatEditWindow, self).__init__()

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
        self.setFixedSize(150,300)
        
        layout = QVBoxLayout()

        text = QLabel('Mitglieder auswaehlen:')

        self.Btn = QPushButton('Aendern')
        self.Btn.clicked.connect(self.updateMembers)

        self.CancelBtn = QPushButton('Abbrechen')
        self.CancelBtn.clicked.connect(self.close)

        ContactScroll = QScrollArea()
        ContactScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        ContactScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ContactScroll.setWidgetResizable(False)
        ContactScroll.setMinimumSize(30,200)

        ContactScrollContainer = QWidget()
        
        ContactListLayout = QVBoxLayout()

        self.CheckBoxList = {}

        sortedList = sorted(self.contactList.items(), key= lambda x: x[1]['name'].lower())

        for c in sortedList:

            contact = c[1]

            cLayout = QHBoxLayout()
            cLabel = QLabel(contact['name'])

            cCheck = QCheckBox()
            if contact['UID'] in self.members:
                cCheck.setCheckState(Qt.Checked)

            self.CheckBoxList[contact['UID']] = cCheck

            cLayout.addWidget(cLabel)
            cLayout.addStretch(1)
            cLayout.addWidget(cCheck)

            ContactListLayout.addLayout(cLayout)

        ContactScrollContainer.setLayout(ContactListLayout)

        ContactScroll.setWidget(ContactScrollContainer)

        layout.addWidget(text)
        layout.addWidget(ContactScroll)
        layout.addWidget(self.Btn)
        layout.addWidget(self.CancelBtn)

        self.setLayout(layout)

    def updateMembers(self):

        statusList = []
        oneUserInList = False
        statusList.append('UID:'+ self.parent.UID + ",1")
        for uid in self.CheckBoxList:
            status = self.CheckBoxList[uid].isChecked()
            statusStatement = "UID:" + uid
            if status:
                statusStatement += ",1"
                oneUserInList = True
            else:
                statusStatement += ",0"

            statusList.append(statusStatement)
        #print(statusList)
        if oneUserInList:
            self.sendMemberList(statusList)
            self.close()

    def sendMemberList(self, statusList):
        req = "UPDATEGROUP\r\n"
        req += "GID:" + self.GID + "\r\n"
        req += '\r\n'.join(statusList)
        req += '\r\n'

        self.tcp.sendReq(req)


        