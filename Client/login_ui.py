
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from ClassConnect import TcpClient
from register_ui import RegisterWindow
from forgetpw_ui import ForgetPwWindow
from main_ui import MainWindow
from Sound import Sound
import time

 
class LoginWindow(QWidget):
   
    def __init__(self, ip=None, port=None, parent=None):
        super(LoginWindow, self).__init__()

        # Perform Tcp Connection
        self.tcp = TcpClient(ip, port)
        self.tcp.recvAns.connect(self.parseAns)
        # Connect errorhandling
        self.tcp.ConError.connect(self.tcpError)
        self.tcp.connected.connect(self.tcpConnected)
        # Setup reconnect Timer
        self.rconTimer = QTimer(self)
        self.rconTimer.timeout.connect(self.tryReconnect)
        # Create Sound Object
        self.sound = Sound()

        # init userData
        self.userName = None
        self.passwd = None
        self.StatusUSER = False
        self.StatusPASS = False
        self.conStat=False
        self.SID = None
        self.UID = None

        # Adjust Window ----------------------------------------------
        # Set Title
        self.setWindowTitle('PySIMS')
        # Set Windwo Icon
        self.setWindowIcon(QIcon('img/pysims_icon_16.png')) 
        self.setFixedSize(200,350)

        # Create widgets ---------------------------------------------
        # Create Logo
        self.logo = QPixmap('img/pysims_logo.png')
        self.logoLabel = ClickableLabel(self)
        self.logoLabel.setPixmap(self.logo)

        # Create Forgot Password
        self.forgotPassLabel = ClickableLabel("<font size=10px>Passwort vergessen?</font>")
        #self.forgotPassLabel.set
        # Create Sign Up
        self.SignUpLabel = ClickableLabel("<font size=10px>Registrieren</font>")

        # Create Message Label
        self.messageLabel = QLabel()

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
        layout.addWidget(self.messageLabel)
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
        
        if(self.conStat==True):
            self.sendUser()

    # Send Username to Server
    def sendUser(self):
        self.userName = self.usernameEdit.text()
        self.passwd = self.passwordEdit.text()
        if self.userName and self.passwd:     
            print ("Send Username")#: %s" % self.userName)
            
            # Show loader animation
            self.loader = QMovie('img/loader.gif')
            self.logoLabel.setMovie(self.loader)
            self.loader.start()

            req = 'USER ' + self.userName + '\r\n'
            self.tcp.sendReq(req)
        elif not self.userName:
            self.wrongData('USER')
        elif not self.passwd: 
            self.wrongData('PASS')

    # Send Password to Server
    def sendPass(self):
        self.passwd = self.passwordEdit.text()
        if self.passwd:
            print ("Send Password")#: %s" % self.passwd)

            req = 'PASS ' + self.passwd + '\r\n'
            self.tcp.sendReq(req)

    # If all Data is correct the user will be logged in
    def login(self):
        self.sound.login()
        self.window = MainWindow(parent=self)
        self.window.setAttribute(Qt.WA_DeleteOnClose)
        self.window.show()

        self.close()

    # If there is wrong Data the Labels are colored Red
    def wrongData(self, data):
        self.logoLabel.setPixmap(self.logo)
        if data == 'USER':
            self.usernameLabel.setText("<font color=red>Benutzername:</font>")

        elif data == 'PASS':
            self.passwordLabel.setText("<font color=red>Passwort:</font>")


    # Send ForgotPass to Server
    def forgotPass(self):
        #print ("Username: %s" % self.usernameEdit.text())   
        #pass
        self.ForgetPwWindow=ForgetPwWindow(parent=self)
        self.ForgetPwWindow.show()

    # Call register Routine
    def register(self):

        self.RegWindow = RegisterWindow(parent=self)
        #RegWindow.setAttribute(Qt.WA_DeleteOnClose)
        self.RegWindow.exec_()

        #print ("Username: %s" % self.usernameEdit.text())

    # Abbort Login (TODO)
    def logoClick(self):
        print ("Logo geklickt!")
        # Show normal Logo
        self.logoLabel.setPixmap(self.logo)

    # Parse Answer from Server
    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):
        #print ('--------LastReq: ', lastReq, ' Ans: ', ans)
        lastCommand = lastReq.split()

        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            #print (lastCommand)
            #print (ans)
            
            # Answer = USER?
            if ans[0] == 'USER OK':
                # USER is accepted
                print ('USER accepted')
                self.StatusUSER = True
                self.usernameLabel.setText("<font color=black>Benutzername:</font>")
                self.sendPass()
                
            elif ans[0] == 'USER ERR':
                self.wrongData('USER')
                self.StatusUSER = False
                print ('USER denied')

            # Answer = PASS? and USER was allready accepted              
            elif ans[0] == 'PASS OK' and self.StatusUSER:
                # PASS is accepted
                print ('PASS accepted')
                self.passwordLabel.setText("<font color=black>Passwort:</font>")
                self.StatusPASS = True
                UID = ans[1].split(':')
                SID = ans[2].split(':')

                if UID[0] == 'UID':
                    self.UID = UID[1]

                if SID[0] == 'SID':
                    self.SID = SID[1]
                    self.login()

            elif ans[0] == 'PASS ERR':
                self.wrongData('PASS')
                self.StatusPASS = False
                print ('PASS denied')

            elif ans[0] == '':
                pass

    def tcpError(self, err):
        # React to connectionerror
        if err == 'ConnectionRefused' or err == 'ConnectionClosed':
            # Show Error Mesasge to User
            self.messageLabel.setText("<font color=red>Server nicht erreichbar!</font>")
            # Close Failed Connection
            self.tcp.abort()
            # Disable Buttons
            self.loginBtn.setEnabled(False)
            self.conStat=False
            # Start timer
            self.rconTimer.start(5000)
        print(err)

    def tryReconnect(self):
        # Try to reach the Server
        self.rconTimer.stop()
        self.messageLabel.setText("<font color=red>Verbinung wird aufgebaut...</font>")
        self.tcp.con()

    def tcpConnected(self):
        # TCP Connection was successful
        # Stop timer
        self.rconTimer.stop()
        self.logoLabel.setPixmap(self.logo)
        # Enable Login Funktions again
        self.messageLabel.setText('')
        self.loginBtn.setEnabled(True)
        self.conStat=True



 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = LoginWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
