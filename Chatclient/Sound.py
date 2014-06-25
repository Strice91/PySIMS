import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Sound(object):
	def __init__(self):
		self.msgSound = QSound('sound/newmsg.wav')
		self.msgSound = QSound('sound/')

	def newMsg(self):
		self.msgSound.play()

	def

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sound = Sound()
    sound.newMsg()
    sys.exit(app.exec_())