from PySide.QtGui import *
from PySide.QtCore import *

class ClickableLabel(QLabel):
 
    def __init(self, parent):
        QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))