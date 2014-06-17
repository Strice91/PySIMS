
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from loginAction import *
from ClassConnect import TcpClient
 
class LoginWindow(QWidget):
   
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        self.tcp = TcpClient()
        self.Act = LoginAction(self)
        self.tcp.recvAns.connect(self.parseAns)
        self.userName = ''
        self.passwd = ''
        self.StatusUSER = False
        self.StatusPASS = False
        self.SID = ''

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
        self.usernameEdit = QLineEdit("test")
        self.usernameLabel = QLabel("Benutzername:")

        # Create Password Input
        self.passwordEdit = QLineEdit("test")
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
        self.loginBtn.clicked.connect(self.startMainWindow)
        # Add mouseReleaseEvent to forgotPass Slot
        self.connect(self.forgotPassLabel, SIGNAL('clicked()'),self.forgotPass)
        # Add mouseReleaseEvent to register Slot
        self.connect(self.SignUpLabel, SIGNAL('clicked()'),self.register)

        self.connect(self.logoLabel, SIGNAL('clicked()'),self.logoClick)  

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


    # Send ForgotPass to Server
    def forgotPass(self):
        print ("Username: %s" % self.usernameEdit.text())   
        LoginAction.requestPass(self)

    # Call register Routine
    def register(self):
        print ("Username: %s" % self.usernameEdit.text())
        LoginAction.registerUser(self)

    def logoClick(self):
        print ("Logo geklickt!")
        # Show normal Logo
        self.logoLabel.setPixmap(self.logo)
        LoginAction.abbortLogin(self)

    @Slot(str, str)
    def parseAns(self, lastReq, ans):
        #print ('--------LastReq: ', lastReq, ' Ans: ', ans)
        lastCommand = lastReq.split()
        lastAns = ans.split()

        #print (lastCommand)
        #print (lastAns)

        # Answer = USER?
        if lastAns[0] == 'USER':
            # USER is accepted
            if lastAns[1] == 'OK':
                print ('USER accepted')
                self.StatusUSER = True
                self.sendPass()
                
            else:
                print ('USER denied')

        # Answer = PASS? and USER was allready accepted              
        elif lastAns[0] == 'PASS' and self.StatusUSER:
            # PASS is accepted
            if lastAns[1] == 'OK':
                print ('PASS accepted')
                self.StatusPASS = True
                SID = lastAns[2].split(':')

                if SID[0] == 'SID':
                    self.SID = SID[1]
            else:
                print ('PASS denied')

        #print ('USER Status: ', self.StatusUSER)
        #print ('PASS Status: ', self.StatusPASS)
        #print ('SID: ', self.SID)

    def startMainWindow(self):
        pass
        #window = QMainWindow(self)
        #window.setAttribute(Qt.WA_DeleteOnClose)
        #window.setWindowTitle(self.tr('Hauptfenster'))
        #window.show()
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = LoginWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())