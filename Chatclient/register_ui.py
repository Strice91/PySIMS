import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from os import path
import TextTools

class RegisterWindow(QWidget):

    def __init__(self, parent=None):
        super(RegisterWindow, self).__init__(parent)
        # Set Title
        self.setWindowTitle('Registrierung')

        # Create Username Input
        self.usernameEdit = QLineEdit("test")
        self.usernameLabel = QLabel("Benutzername:")

        # Create Password Input
        self.passwordEdit = QLineEdit("test")
        self.passwordLabel = QLabel("Passwort:")
        # Set Password Input to not readable
        self.passwordEdit.setEchoMode(QLineEdit.Password)


        # Create Password Confirmation
        self.passwordConEdit = QLineEdit("test")
        self.passwordConLabel = QLabel("Passwort wiederholen:")
        # Set Password Confirmation to not readable
        self.passwordConEdit.setEchoMode(QLineEdit.Password)

        # Create Email Input
        self.emailEdit = QLineEdit("test@test.test")
        self.emailLabel = QLabel("E-Mail:")

        # Create Login Button
        self.regBtn = QPushButton("Registrieren")

        # Build Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.passwordConLabel)
        layout.addWidget(self.passwordConEdit)
        layout.addWidget(self.emailLabel)
        layout.addWidget(self.emailEdit)
        layout.addWidget(self.regBtn)


        #Set dialog layout
        self.setLayout(layout)




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = RegisterWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())



