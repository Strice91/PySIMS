
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from login_ui import LoginWindow

class MainProgram(QApplication):
    
    def __init__(self, parent=None):
        super(MainProgram, self).__init__(sys.argv)   

        self.startProgramm()

    def startProgramm(self):
        try:
            # Check if IP and Port are declared
            server_ip = sys.argv[1]
            server_port = int(sys.argv[2])
            self.Log = LoginWindow(server_ip, server_port, parent=self)
        except:
            # Start Programm without parameters
            self.Log = LoginWindow(parent=self)
        self.Log.show()  


if __name__ == '__main__':
    prog = MainProgram()
    sys.exit(prog.exec_())