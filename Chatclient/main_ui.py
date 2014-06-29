import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from chat_ui import QChatWindow
from contacts import contactList
from Sound import Sound
from about import AboutWindow
#import login_ui
from os import path
import time

 
class MainWindow(QMainWindow):

    openChat = Signal(str)
    newMsg = Signal(str, str)

    # Cunstructor of MainWindow ##############################################

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.parent = parent

        self.tcp = parent.tcp
        self.tcp.recvAns.connect(self.parseAns)
        self.tcp.ConError.connect(self.tcpError)

        self.UID = parent.UID
        self.sound = Sound()
        self.initUI()
        
    # Init Functions #########################################################
    def initUI(self):

        # Write all Stylsheets
        self.setStyle()
        # Init the Profile Groupbox
        self.Profile()
        # Init the Contro Groupbox
        #self.Control()
        # Init the Contact Groupbox
        self.Contacts()
        # Request Contact List from Server
        #self.requestList()
        # Requste Stored Messages from Server
        self.requestMsg()
        # Init List of Chatwindows
        self.ChatWindows = {}


        # Adjust Window ------------------------------------------------------
        # Set Title
        self.setWindowTitle('PySIMS')
        # Set Windwo Icon
        self.setWindowIcon(QIcon('img/pysims_icon_16.png')) 
        # Set Window Position and Size
        self.setGeometry(10, 50, 250, 400)
        self.setFixedWidth(250)

        # Show Statusbar
        self.statusBar().showMessage('Verbinung hergestellt')

        # MenuBar ------------------------------------------------------------
        # Create Exit
        exitAction = QAction(QIcon('img/main/exit.png'), 'Beenden', self)
        exitAction.setStatusTip('Beenden')
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        # Create Profil
        profileAction = QAction(QIcon('img/main/profile.png'), 'Profil', self)
        profileAction.setStatusTip('Benutzer Profil')
        profileAction.setShortcut('Ctrl+P')
        #profileAction.triggered.connect(self.close)

        # Create Settings
        settingsAction = QAction(QIcon('img/main/settings.png'), 'Einstellungen', self)
        settingsAction.setStatusTip('Einstellungen')
        settingsAction.setShortcut('Ctrl+E')
        #settingsAction.triggered.connect(self.close)

        # Create About
        aboutAction = QAction(QIcon('img/main/about.png'), 'Ueber PySIMS', self)
        aboutAction.setStatusTip('Ueber PySIMS')
        aboutAction.triggered.connect(self.openAboutWindow)

        # Create Help
        helpAction = QAction(QIcon('img/main/help.png'), 'Hilfe', self)
        helpAction.setStatusTip('Hilfe')
        #settingsAction.triggered.connect(self.close)

        # Create MenuBar
        menubar = self.menuBar()
        # Add File Menu
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addAction(exitAction)
        # Add Options Menu
        optMenu = menubar.addMenu('&Optionen')
        optMenu.addAction(profileAction)
        optMenu.addAction(settingsAction)
        # Add Help Menu
        helpMenu = menubar.addMenu('&Hilfe')
        helpMenu.addAction(helpAction)
        helpMenu.addAction(aboutAction)


        # Create layout and add widgets --------------------------------------

        widget = QWidget()
        self.setCentralWidget(widget)

        # Build Main Layout, Add all Widgets
        layout = QVBoxLayout()
        #layout.addWidget(scroll)
        layout.addWidget(self.ProfileGroup)
        #layout.addWidget(self.ControlGroup)
        layout.addWidget(self.ContactGroup)
        layout.addStretch(1)

        widget.setLayout(layout)

    def setStyle(self):

        self.setStyleSheet( """
                            QLabel[labelClass='Username'] 
                            {font-size: 16px;

                            }
                            """)

    def Contacts(self):

        # Create Contact Group Box
        self.ContactGroup = QGroupBox('Kontakte')
        # Create Main Layout
        layout = QVBoxLayout()
        # Create Scroll Area
        self.ContactScroll = QScrollArea()
        # Scroll Area Properties
        self.ContactScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ContactScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ContactScroll.setWidgetResizable(False)
        self.ContactScroll.setMinimumSize(30,300)

        # Create a Container Widget for the VBoxLayout
        self.ContactScrollContainer = QWidget()
        # Create the Contactlist
        self.ContactListLayout = QVBoxLayout()
        # Add Scroll Area to Layout
        layout.addWidget(self.ContactScroll)
        # Add Layout to Group
        self.ContactGroup.setLayout(layout)

    def Profile(self):

        # Create the Profile Groupbox
        self.ProfileGroup = QGroupBox('Profil')

        # Create the Profile Main Layout
        ProfileLayout = QHBoxLayout()

        # Create Profile Information Layout
        ProfileInfoLayout = QVBoxLayout()

        # Create username Label
        self.userNameLabel = QLabel(self.parent.userName)
        self.userNameLabel.setProperty('labelClass', 'Username')

        # Create Status selector
        self.statusSelect = QComboBox(self)
        self.statusSelect.addItem('Online')
        self.statusSelect.addItem('Abwesend')
        self.statusSelect.addItem('Beschaeftigt')
        self.statusSelect.addItem('Offline')

        self.statusSelect.currentIndexChanged[int].connect(self.changeStatus)

        # Create Infotext Label
        self.ProfileinfoLabel = QLabel('<font color=green>Verbunden</font>')

        # Create Profile Picture
        self.UserImgPixmap = QPixmap('img/user/userpic.png')
        self.UserImgLabel = ClickableLabel(self)
        self.UserImgLabel.setPixmap(self.UserImgPixmap)
        
        # Build Profile Info Layout
        ProfileInfoLayout.addWidget(self.userNameLabel)
        ProfileInfoLayout.addWidget(self.statusSelect)
        ProfileInfoLayout.addWidget(self.ProfileinfoLabel)

        # Build Profile Main Layout
        ProfileLayout.addLayout(ProfileInfoLayout)
        ProfileLayout.addStretch(1)
        ProfileLayout.addWidget(self.UserImgLabel)

        # Add to Profile Group
        self.ProfileGroup.setLayout(ProfileLayout)

    def Control(self):

        self.ControlGroup = QGroupBox('Control')
        # Create the Control Main Layout
        ControlLayout = QHBoxLayout()


    # Actions and Slots ######################################################

    def updateContacts(self, contactList):

        sortedList = sorted(contactList.items(), key= lambda x: x[1]['name'].lower())

        self.ContactScrollContainer.deleteLater()
        self.ContactScrollContainer = QWidget()
        self.ContactListLayout = None
        self.ContactListLayout = QVBoxLayout()

        for c in sortedList:

            contact = c[1]
            cLayout = QHBoxLayout()

            cLabel = QLabel(contact['name'])
            cLabel.setMinimumSize(QSize(100,24))
            cLabel.setStyleSheet("QLabel {font-size: 14px}")

            StatusImgPath = path.join('img/user/',contact['status'] +'.png')
            cStatusPixmap = QPixmap(StatusImgPath)
            cStatus = QLabel()
            cStatus.setToolTip(contact['status'])
            cStatus.setPixmap(cStatusPixmap)

            cChatPixmap = QPixmap('img/main/chat.png')
            cChat = ClickableChat(self, contact['UID'])
            cChat.setPixmap(cChatPixmap)
            cChat.setToolTip('Chat beginnen')
            cChat.openChat.connect(self.openChat)

            cLayout.addWidget(cLabel)
            cLayout.addStretch(1)
            cLayout.addWidget(cStatus)
            cLayout.addWidget(cChat)

            self.ContactListLayout.addLayout(cLayout)
            
        # Add Contactlist to Container
        self.ContactScrollContainer.setLayout(self.ContactListLayout)
        # Add Container to Scroll Area
        self.ContactScroll.setWidget(self.ContactScrollContainer) 

    def openAboutWindow(self):
        self.AboutWindow = AboutWindow(parent=self)
       
        self.AboutWindow.exec_()

    def requestList(self):
        req = 'GETLIST'
        self.tcp.sendReq(req)

    def requestMsg(self):
        req = 'PULLMSGS'
        self.tcp.sendReq(req)

    def requestGID(self, members):
        req = 'MKGRP\r\n'
        req += 'UID:'
        for userID in members:
            if not userID == members[-1]:
                req += userID + ','
            else:
                req += userID + '\r\n'

        req += 'SID:' + self.parent.SID + '\r\n\r\n'

        self.tcp.sendReq(req)

    def sendAck(self):
        #self.tcp.sendReq('ACK\r\n')
        #print('ACK sent')
        pass

    def changeStatus(self, status):

        if status == 0:
            # Online
            print('New Status: Online')
        elif status == 1:
            # Abwesend
            print('New Status: Abwesend')
        elif status == 2:
            # Beschaeftigt
            print('New Status: Beschaeftigt')
        elif status == 3:
            # Offline
            print('New Status: Offline')

    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):

        dlvmsg = False
        gids = {}

        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            print('------  Main Window Recived: -----')
            print(ans)
            print('----------------------------------')

            if ans[0] == 'USRLIST':
                myContacts = contactList(ans[1:], self.parent.userName)
                self.contactList = myContacts.getList()
                self.updateContacts(self.contactList)

            if ans[0] == 'MKGRP OK':
                GID = ans[1].split(':')
                if GID[0] == 'GID':
                    self.checkChatWindow(GID[1])
            
            if ans[0] == 'DLVMSG':
                GID = ans[1].split(':')
                UID = ans[2].split(':')
                if GID[0] == 'GID':
                    if GID[1] in gids:
                        if UID[0] == 'UID':
                            gids[GID[1]]['UIDS'].append(UID[1])
                            gids[GID[1]]['MSGS'].append(ans[3])
                    else:
                        if UID[0] == 'UID':
                            gids[GID[1]] = {'UIDS': [], 'MSGS': []}
                            gids[GID[1]]['UIDS'].append(UID[1])
                            gids[GID[1]]['MSGS'].append(ans[3])
                        


        if gids:
            for gid in gids:
                print(gids[gid])
                #self.sendAck()
                self.checkChatWindow(gid, gids[gid]['UIDS'], gids[gid]['MSGS'])
                self.sound.newWindow()

                    

    @Slot(str)
    def openChat(self, memberID):
        print('Open Chat with', memberID)
        members = [self.UID, memberID] 
        self.requestGID(members)

    def checkChatWindow(self, gid, senderID=None, msg=None):

        #print('SenderID:', senderID)
        if gid in self.ChatWindows:
            pass
            #print (self.ChatWindows[gid])
        else:
            self.ChatWindows[gid] = QChatWindow(gid, senderID, msg, self)
            self.ChatWindows[gid].show()

    @Slot(str)
    def tcpError(self, err):
        if err == 'ConnectionClosed':
            self.statusBar().showMessage('Verbinung unterbrochen!')
            self.ProfileinfoLabel.setText('<font color=red>Verbinung unterbrochen!</font>')
        elif err == 'ConnectionRefused':
            self.statusBar().showMessage('Server nicht erreichbar!')
            self.ProfileinfoLabel.setText('<font color=red>Server nicht erreichbar!</font>')
        self.logout()

    def logout(self):
        self.sound.conError()
        self.parent.show()
        #self.Log = login_ui.LoginWindow()
        #self.Log.show()

        self.close()

    def closeEvent(self, ev):

        gids = []
        for gid in self.ChatWindows:
            gids.append(gid)

        for gid in gids:
            self.ChatWindows[gid].close() 

    ##########################################################################


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(app.exec_())
