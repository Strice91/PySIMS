import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from chat_ui import QChatWindow
from loginAction import *
from contacts import contactList
from os import path



class ControllWidget(QWidget):
    def __init__(self):
        super(ControllWidget, self).__init__()

        pass


class ContactWidget(QWidget):
    def __init__(self):
        super(ContactWidget, self).__init__()

        pass

 
class MainWindow(QMainWindow):

    openChat = Signal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def setStyle(self):

        self.setStyleSheet( """
                            QLabel[labelClass='Username'] 
                            {font-size: 16px;

                            }
                            """)

    def Contacts(self, contactList):
        # Create Contact Group Box
        self.ContactGroup = QGroupBox('Kontakte')
        # Create Main Layout
        layout = QVBoxLayout()
        # Create Scroll Area
        ContactScroll = QScrollArea()
        # Scroll Area Properties
        ContactScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        ContactScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ContactScroll.setWidgetResizable(False)
        # Create a Container Widget for the VBoxLayout
        ContactScrollContainer = QWidget()
        # Create the Contactlist
        self.ContactListLayout = QVBoxLayout()

        for uid in contactList:
            contact = contactList[uid]
            cLayout = QHBoxLayout()

            cLabel = QLabel(contact['name'])
            cLabel.setStyleSheet("QLabel {font-size: 14px}")

            StatusImgPath = path.join('img/user/',contact['status'] +'.png')
            cStatusPixmap = QPixmap(StatusImgPath)
            cStatus = QLabel()
            cStatus.setPixmap(cStatusPixmap)

            cChatPixmap = QPixmap('img/user/chat.png')
            cChat = ClickableChat(self, uid)
            cChat.setPixmap(cChatPixmap)
            cChat.openChat.connect(self.openChat)

            cGroupPixmap = QPixmap('img/user/add_group.png')
            cGroup = ClickableLabel(self)
            cGroup.setPixmap(cGroupPixmap)

            cLayout.addWidget(cLabel)
            cLayout.addStretch(1)
            cLayout.addWidget(cStatus)
            cLayout.addWidget(cChat)
            cLayout.addWidget(cGroup)

            self.ContactListLayout.addLayout(cLayout)


        # Add Contactlist to Container
        ContactScrollContainer.setLayout(self.ContactListLayout)
        # Add Container to Scroll Area
        ContactScroll.setWidget(ContactScrollContainer)
        # Add Scroll Area to Layout
        layout.addWidget(ContactScroll)
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
        self.userNameLabel = QLabel('Franz Xaver')
        self.userNameLabel.setProperty('labelClass', 'Username')

        # Create Status selector
        self.statusSelect = QComboBox(self)
        self.statusSelect.addItem('Online')
        self.statusSelect.addItem('Abwesend')
        self.statusSelect.addItem('Beschäftigt')
        self.statusSelect.addItem('Offline')

        # Create Infotext Label
        self.ProfileinfoLabel = QLabel('Infotext 04.05.14')

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


    def initUI(self):

        self.Profile()
        self.setStyle()
        myContacts = contactList(20)
        self.contactList = myContacts.getList()
        self.ChatWindows = {}

        self.Contacts(self.contactList)

        # Adjust Window ----------------------------------------------
        # Set Title
        self.setWindowTitle('PySIMS')
        # Set Windwo Icon
        self.setWindowIcon(QIcon('img/pysims_icon_16.png')) 
        # Set Window Position and Size
        self.setGeometry(300, 300, 250, 600)
        # Show Statusbar
        self.statusBar().showMessage('Ready')

        # MenuBar ----------------------------------------------------
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
        aboutAction = QAction(QIcon('img/main/about.png'), 'Über PySIMS', self)
        aboutAction.setStatusTip('Über PySIMS')
        #settingsAction.triggered.connect(self.close)

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


        # Create layout and add widgets ------------------------------

        widget = QWidget()
        self.setCentralWidget(widget)

        # Build Main Layout
        layout = QVBoxLayout()
        #layout.addWidget(scroll)
        layout.addWidget(self.ProfileGroup)
        layout.addWidget(self.ContactGroup)
        layout.addStretch(1)

        widget.setLayout(layout)

    @Slot(str)
    def openChat(self, uid):
        print('Open Chat with', uid)
        self.ChatWindows[uid] = QChatWindow(self.contactList[uid])
        self.ChatWindows[uid].show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainW = MainWindow()
    mainW.show()
    sys.exit(app.exec_())