import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from LabelExtension import *
from os import path

class AboutWindow(QDialog):

    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        # Parent
        self.parent = parent

        self.setWindowTitle('Über')
        self.setFixedSize(150,220)

        # Create Logo
        self.logo = QPixmap('img/pysims_logo.png')
        self.logoLabel = ClickableLabel(self)
        self.logoLabel.setPixmap(self.logo)

        self.TeamLabel=QLabel("Gruppe4:")
        self.TeamNameLabel=QLabel("Alexander Kosch\nDaniel Orthofer\nLaurenz Henkel\nStefan Röhrl")

        layout = QVBoxLayout()
        layout.addWidget(self.logoLabel)
        layout.addWidget(self.TeamLabel)
        layout.addWidget(self.TeamNameLabel)



        #Set dialog layout
        self.setLayout(layout)

        




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    login = AboutWindow()
    login.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
