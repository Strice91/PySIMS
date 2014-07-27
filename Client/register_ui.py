import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from os import path
import TextTools

class RegisterWindow(QDialog):

    def __init__(self, parent=None):
        super(RegisterWindow, self).__init__(parent)
        # Parent
        self.parent = parent
        self.tcp = parent.tcp

        # Connect the incoming TCP Signal with parseAns
        self.tcp.recvAns.connect(self.parseAns)

        # Set Title
        self.setWindowTitle('Registrierung')

        # Create Username Input
        self.usernameEdit = QLineEdit("")
        self.usernameLabel = QLabel("Benutzername:")

        # Create Password Input
        self.passwordEdit = QLineEdit("")
        self.passwordLabel = QLabel("Passwort:")
        # Set Password Input to not readable
        self.passwordEdit.setEchoMode(QLineEdit.Password)


        # Create Password Confirmation
        self.passwordConEdit = QLineEdit("")
        self.passwordConLabel = QLabel("Passwort wiederholen:")
        # Set Password Confirmation to not readable
        self.passwordConEdit.setEchoMode(QLineEdit.Password)

        # Create SecQues Input
        self.squesEdit = QLineEdit("")
        self.squesLabel = QLabel("Sicherheitsfrage:")
        self.sansEdit = QLineEdit("")
        self.sansLabel = QLabel("Antwort:")

        # Create Login Button
        self.regBtn = QPushButton("Registrieren")

        # Create Hintlabel
        self.Hint=QLabel("")

        # Build Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.passwordConLabel)
        layout.addWidget(self.passwordConEdit)
        layout.addWidget(self.Hint)
        layout.addWidget(self.squesLabel)
        layout.addWidget(self.squesEdit)
        layout.addWidget(self.sansLabel)
        layout.addWidget(self.sansEdit)
        layout.addWidget(self.regBtn)


        #Set dialog layout
        self.setLayout(layout)

        # Add button signal to sendLogin slot
        self.regBtn.clicked.connect(self.sendRegister)
    
    def sendRegister(self):
        
        self.userName    = self.usernameEdit.text() 
        self.password    = self.passwordEdit.text()
        self.passwordCon = self.passwordConEdit.text()
        self.sques       = self.squesEdit.text()
        self.sans        = self.sansEdit.text()
        
        if (self.password):
            if (self.password==self.passwordCon):
                #print("RICHTIG")
                if(self.sques):
                    if(self.sans):
                        req = 'REGISTER ' + self.userName + ' ' + self.password + '\r\n' + self.sques + '\r\n' + self.sans + '\r\n\r\n'
                        self.tcp.sendReq(req)
    
            else:
                print("FALSCH")
                self.Hint.setText(u"<font color=red>Passwoerter nicht gleich</font>")


    @Slot(str, str)
    def parseAns(self, lastReq, ans):
        lastCommand = lastReq.split()
        
        if(ans=="REGISTER OK\r\n"):
            self.parent.usernameEdit.setText(self.userName)
            self.parent.passwordEdit.setText(self.password)
            self.close()
        
        elif(ans=="REGUSER ERR\r\n"):
            self.Hint.setText("<font color=red>Benutzername vergeben</font>")

        




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = RegisterWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())



