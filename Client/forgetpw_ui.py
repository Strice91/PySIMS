from PySide.QtCore import *
from PySide.QtGui import *
import sys

class ForgetPwWindow(QDialog):
    def __init__(self, parent=None):
        super(ForgetPwWindow, self).__init__(parent)
        # Parent
        self.parent = parent
        self.tcp = parent.tcp
        

        self.tcp.recvAns.connect(self.parseAns)

        layout = QVBoxLayout()

        
        # Set Title
        self.setWindowTitle('Passwort vergessen')

        # Create Username Input
        self.usernameEdit = QLineEdit("")
        self.usernameLabel = QLabel("Benutzername:")



        # Create Login Button
        self.forgBtn = QPushButton("Passwort vergessen")
 

        # Create Hintlabel
        self.Hint=QLabel("")

        # Build Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameEdit)

        layout.addWidget(self.forgBtn)
        layout.addWidget(self.Hint)


        #Set dialog layout
        self.setLayout(layout)


        self.forgBtn.clicked.connect(self.sendforget)

    def sendforget(self):
        self.userName= self.usernameEdit.text()
        
        if(self.userName):
            req= 'FORGOTPASS ' + self.userName +'\r\n'
            self.tcp.sendReq(req)
        

    def Window2open(self):
        print("TEST")

        
        self.secq = SecQuestion(parent=self)
        self.secq.setWindowTitle(self.tr('Sicherheitsfrage'))
        self.close()
        self.secq.show()


        #self.close()
    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):
        lastCommand = lastReq.split()
        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            #print("BLABLABLA")
            #print("ANSWER:")
            #print(
            
            if(ans[0]=="FORGOTPASS OK"):
                self.sques=ans[1]
                self.Window2open()
            
    


class SecQuestion(QDialog):
    def __init__(self, parent=None):
        super(SecQuestion, self).__init__(parent)
        
        self.parent = parent        
        self.tcp = parent.tcp
        self.tcp.recvAns.connect(self.parseAns)

        self.sques=parent.sques
        layout = QVBoxLayout()
        self.Btn = QPushButton('Abschicken')

        self.secLabel = QLabel("Sicherheitsfrage:")
        self.secquestionLabel = QLabel(self.sques)

        self.secAnsLabel = QLabel("Antwort:")
        self.secAnsEdit = QLineEdit("")

        layout.addWidget(self.secLabel)
        layout.addWidget(self.secquestionLabel)
        layout.addWidget(self.secAnsLabel)        
        layout.addWidget(self.secAnsEdit)
        layout.addWidget(self.Btn)


        #Set dialog layout
        self.setLayout(layout)


        self.Btn.clicked.connect(self.sendCheckAnswer)

    def sendCheckAnswer(self):
        
        self.secAns=self.secAnsEdit.text()
        
        if(self.secAns):
            req='CHECKANSWER '+ self.secAns +'\r\n'
            self.tcp.sendReq(req)
        

    def Window3open(self):
        print("test")

        self.conPW = ConfirmPassWord(parent=self)
        self.conPW.setWindowTitle(self.tr('Passwort zuruecksetzen'))
        self.close()
        self.conPW.show()

    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):
        lastCommand = lastReq.split()
        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            if(ans[0]=="ANSWER OK"):
                self.Window3open()



class ConfirmPassWord(QDialog):
    def __init__(self, parent=None):
        super(ConfirmPassWord, self).__init__(parent)

        self.parent = parent
        self.tcp = parent.tcp
        self.tcp.recvAns.connect(self.parseAns)


        layout = QVBoxLayout()
        self.passwordEdit = QLineEdit("")
        self.passwordLabel = QLabel("Passwort:")
        # Set Password Input to not readable
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.Btn = QPushButton('Zurücksetzen')

        # Create Password Confirmation
        self.passwordConEdit = QLineEdit("")
        self.passwordConLabel = QLabel("Passwort wiederholen:")
        # Set Password Confirmation to not readable
        self.passwordConEdit.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.passwordConLabel)        
        layout.addWidget(self.passwordConEdit)
        layout.addWidget(self.Btn)


        #Set dialog layout
        self.setLayout(layout)

        self.Btn.clicked.connect(self.sendChangePass)

    def sendChangePass(self):
        self.pw  = self.passwordEdit.text()
        self.pwc = self.passwordConEdit.text()

        if(self.pw):
            if(self.pw==self.pwc):
                req= 'CHANGEPASS '+self.pw+'\r\n'
                self.tcp.sendReq(req)


    @Slot(str, str)
    def parseAns(self, lastReq, ServerAns):
        lastCommand = lastReq.split()
        for ans in ServerAns.split('\r\n\r\n'):
            ans = ans.split('\r\n')
            
            if(ans[0]=="CHANGEPASS OK"):
                self.close()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ForgetPwWindow()
    w.show()
    sys.exit(app.exec_())
