import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Sound(object):
	""" Creates all sounds that can be played in PySIMS."""

	def __init__(self):
		# Load all soundfiles
		self.msgSound = QSound('sound/newMsg.wav')
		self.errorSound = QSound('sound/error.wav')
		self.newWin = QSound('sound/newWindow.wav')
		self.online = QSound('sound/online.wav')

	def newMsg(self):
		# Play the NewMessage Sound
		self.msgSound.play()

	def conError(self):
		# Play the Error Sound
		self.errorSound.play()

	def newWindow(self):
		# Play the NewWindow Sound
		self.newWin.play()

	def login(self):
		# Play the Login Sound
		self.online.play()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    sound = Sound()
    sound.newMsg()
    sys.exit(app.exec_())