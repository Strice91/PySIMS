
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from loginAction import *
 
class LoginWindow(QWidget):
   
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

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
        self.usernameEdit = QLineEdit("Write name here")
        self.usernameLabel = QLabel("Benutzername:")

        # Create Password Input
        self.passwordEdit = QLineEdit()
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
        self.loginBtn.clicked.connect(self.sendLogin)
        self.loginBtn.clicked.connect(self.startMainWindow)
        # Add mouseReleaseEvent to forgotPass Slot
        self.connect(self.forgotPassLabel, SIGNAL('clicked()'),self.forgotPass)
        # Add mouseReleaseEvent to register Slot
        self.connect(self.SignUpLabel, SIGNAL('clicked()'),self.register)

        self.connect(self.logoLabel, SIGNAL('clicked()'),self.logoClick)  

    # Send Login Data to Server
    def sendLogin(self):
        print ("Username: %s" % self.usernameEdit.text())
        print ("Password: %s" % self.passwordEdit.text())
        # Show loader animation
        self.loader = QMovie('img/loader.gif')
        self.logoLabel.setMovie(self.loader)
        self.loader.start()
        LoginAction.loginUser(self)

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

    def startMainWindow(self):
        window = QMainWindow(self)
        window.setAttribute(Qt.WA_DeleteOnClose)
        window.setWindowTitle(self.tr('Hauptfenster'))
        window.show()
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = LoginWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())