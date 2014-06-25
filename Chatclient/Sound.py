import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Sound(object):
	def __init__(self):
		self.msgSound = QSound('sound/newmsg2.wav')
		self.errorSound = QSound('sound/error2.wav')
		self.newWin = QSound('sound/newwindow2.wav')

	def newMsg(self):
		self.msgSound.play()

	def conError(self):
		self.errorSound.play()

	def newWindow(self):
		self.newWin.play()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sound = Sound()
    sound.newMsg()
    sys.exit(app.exec_())