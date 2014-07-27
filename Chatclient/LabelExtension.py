from PySide.QtGui import *
from PySide.QtCore import *

class ClickableLabel(QLabel):
    """ This Lable is Clickable."""
 
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))

class ClickableChat(QLabel):
    """ This Lable can be clicke and
        it emits a Signal with a string
        to pass information about the lable"""

    openChat = Signal(str)

    def __init__(self, parent, uid):
        QLabel.__init__(self, parent)

        self.uid = uid

    def mouseReleaseEvent(self, ev):
        self.openChat.emit(self.uid)