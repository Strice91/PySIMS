import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Sound(object):
	def __init__(self):
		self.msgSound = QSound('sound/newMsg.wav')
		self.errorSound = QSound('sound/error.wav')
		self.newWin = QSound('sound/newWindow.wav')
		self.online = QSound('sound/online.wav')

	def newMsg(self):
		self.msgSound.play()

	def conError(self):
		self.errorSound.play()

	def newWindow(self):
		self.newWin.play()

	def login(self):
		self.online.play()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sound = Sound()
    sound.newMsg()
    sys.exit(app.exec_())