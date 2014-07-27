import sys
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from loginAction import *

class ParentWindow(QWidget):
    def __init__(self, parent=None):
        super(ParentWindow, self).__init__(parent)
        # Set Title
        self.setWindowTitle('Parent Window')
        # Create Login Button
        self.oBtn = QPushButton("Child Window öffnen")
        self.cBtn = QPushButton("Child Window schließen")
        layout = QVBoxLayout()
        layout.addWidget(self.oBtn)
        layout.addWidget(self.cBtn)
        self.setLayout(layout)

        # Add button signal to sendLogin slot
        self.oBtn.clicked.connect(self.openWindow)
        self.cBtn.clicked.connect(self.closeWindow)

    def openWindow(self):
        self.child=ChildWindow()
        #child.show()
        print("öffne Fenster")

    def closeWindow(self):
        self.child.close()
        print("öffne Fenster")
        

class ChildWindow(QWidget):
    def __init__(self):
        super(ChildWindow, self).__init__()
        # Set Title
        self.setWindowTitle('Child Window')
        self.show()
    

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = ParentWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
