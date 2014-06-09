
import sys
from PySide import QtGui
from PySide import QtCore
import login_ui
import ClassConnect

class Example(QtGui.QMainWindow):
    
    def __init__(self, tcp):
        super(Example, self).__init__()              
        
        self.statusBar().showMessage('Ready')
        tcp.sendAns.connect(tcp.myTest)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')    
        #self.show()

    @QtCore.Slot(str)
    def myTest(self, ans):
        print('hi')
        print('Ant:',ans)
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    tcp = ClassConnect.MyTCPClient('localhost', 8075)
    tcp.sendMessage('USER stefan')
    print('main ', tcp.ans)
    ex = Example(tcp)
    login = login_ui.LoginWindow()
    login.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()