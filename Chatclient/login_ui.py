
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from loginAction import *
from ClassConnect import TcpClient
from register_ui import RegisterWindow
from main_ui import MainWindow
import time

 
class LoginWindow(QWidget):
   
    def __init__(self, ip=None, port=None, parent=None):
        super(LoginWindow, self).__init__()

        self.tcp = TcpClient(ip, port)
        self.Act = LoginAction(self)
        self.tcp.recvAns.connect(self.parseAns)
        self.userName = None
        self.passwd = None
        self.StatusUSER = False
        self.StatusPASS = False
        self.SID = None
        self.UID = None

        # Adjust Window ----------------------------------------------
        # Set Title
        self.setWindowTitle('PySIMS')
        # Set Windwo Icon
        self.setWindowIcon(QIcon('img/pysims_icon_16.png')) 

        # Create widgets ---------------------------------------------
        # Create Logo
        self.logo = QPixmap('img/pysims_logo.png')
        self.logoLabel = ClickableLabel(self)
        self.logoLabel.setPixmap(self.logo)

        # Create Forgot Password
        self.forgotPassLabel = ClickableLabel("Passwort vergessen?")

        # Create Sign Up
        self.SignUpLabel = ClickableLabel("Registrieren")

		# Create Username Input
        self.usernameEdit = QLineEdit("")
        self.usernameLabel = QLabel("Benutzername:")

        # Create Password Input
        self.passwordEdit = QLineEdit("")
        self.passwordLabel = QLabel("Passwort:")
        # Set Password Input to not readable
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        # Create Login Button
        self.loginBtn = QPushButton("Login")

        # Create layout and add widgets ------------------------------
        # Build Logo Layout
        hboxLogo = QHBoxLayout()
        hboxLogo.addStretch(1)
        hboxLogo.addWidget(self.logoLabel)
        hboxLogo.addStretch(1)

        # Build Lower Layout
        hboxReg = QHBoxLayout()
        hboxReg.addWidget(self.forgotPassLabel)
        hboxReg.addStretch(1)
        hboxReg.addWidget(self.SignUpLabel)

        # Build Main Layout
        layout = QVBoxLayout()
        layout.addLayout(hboxLogo)
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.loginBtn)
        layout.addLayout(hboxReg)
        # Set dialog layout
        self.setLayout(layout)

        # Signals and Slots ------------------------------------------
        # Add button signal to sendLogin slot
        self.loginBtn.clicked.connect(self.sendUser)
        self.usernameEdit.returnPressed.connect(self.jumpFunction1)
        self.passwordEdit.returnPressed.connect(self.jumpFunction2)
        
        # Add mouseReleaseEvent to forgotPass Slot
        self.connect(self.forgotPassLabel, SIGNAL('clicked()'),self.forgotPass)
        # Add mouseReleaseEvent to register Slot
        self.connect(self.SignUpLabel, SIGNAL('clicked()'),self.register)

        self.connect(self.logoLabel, SIGNAL('clicked()'),self.logoClick)  

    def jumpFunction1(self):
        self.passwordEdit.setFocus()

    def jumpFunction2(self):
        self.sendUser()

    # Send Username to Server
    def sendUser(self):
        self.userName = self.usernameEdit.text()  
        if self.userName:     
            print ("Send Username: %s" % self.userName)
            
            # Show loader animation
            self.loader = QMovie('img/loader.gif')
            self.logoLabel.setMovie(self.loader)
            self.loader.start()

            req = 'USER ' + self.userName
            self.tcp.sendReq(req)

    # Send Password to Server
    def sendPass(self):
        self.passwd = self.passwordEdit.text()
        if self.passwd:
            print ("Send Password: %s" % self.passwd)

            req = 'PASS ' + self.passwd
            self.tcp.sendReq(req)

    def login(self):
        time.sleep(1)

        self.window = MainWindow(parent=self)
        self.window.setAttribute(Qt.WA_DeleteOnClose)
        self.window.setWindowTitle(self.tr('Hauptfenster'))
        self.window.show()

        self.close()

    def wrongData(self, data):
        self.logoLabel.setPixmap(self.logo)
        if data == 'USER':
            self.usernameLabel.setText("<font color=red>Benutzername:</font>")

        elif data == 'PASS':
            self.passwordLabel.setText("<font color=red>Passwort:</font>")


    # Send ForgotPass to Server
    def forgotPass(self):
        print ("Username: %s" % self.usernameEdit.text())   
        LoginAction.requestPass(self)

    # Call register Routine
    def register(self):

        self.RegWindow = RegisterWindow(parent=self)
        #RegWindow.setAttribute(Qt.WA_DeleteOnClose)
        self.RegWindow.exec_()

        print ("Username: %s" % self.usernameEdit.text())
        #LoginAction.registerUser(self)

    def logoClick(self):
        print ("Logo geklickt!")
        # Show normal Logo
        self.logoLabel.setPixmap(self.logo)
        LoginAction.abbortLogin(self)

    @Slot(str, str)
    def parseAns(self, lastReq, ans):
        #print ('--------LastReq: ', lastReq, ' Ans: ', ans)
        lastCommand = lastReq.split()
        lastAns = ans.split('\r\n')

        #print (lastCommand)
        #print (lastAns)

        # Answer = USER?
        if lastAns[0] == 'USER OK':
            # USER is accepted
            print ('USER accepted')
            self.StatusUSER = True
            self.usernameLabel.setText("<font color=black>Benutzername:</font>")
            self.sendPass()
                
        elif lastAns[0] == 'USER ERR':
            self.wrongData('USER')
            self.StatusUSER = False
            print ('USER denied')

        # Answer = PASS? and USER was allready accepted              
        elif lastAns[0] == 'PASS OK' and self.StatusUSER:
            # PASS is accepted
            print ('PASS accepted')
            self.passwordLabel.setText("<font color=black>Passwort:</font>")
            self.StatusPASS = True
            UID = lastAns[1].split(':')
            SID = lastAns[2].split(':')

            if UID[0] == 'UID':
                self.UID = UID[1]

            if SID[0] == 'SID':
                self.SID = SID[1]
                self.login()

        elif lastAns[0] == 'PASS ERR':
                self.wrongData('PASS')
                self.StatusPASS = False
                print ('PASS denied')

        elif lastAns[0] == '':
            pass

        #print ('USER Status: ', self.StatusUSER)
        #print ('PASS Status: ', self.StatusPASS)
        #print ('SID: ', self.SID)

 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = LoginWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
