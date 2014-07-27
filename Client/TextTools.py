import datetime
import time

class TextTools(object):
	""" This function builds the right text setting.
		To display the message text in a proper way
		in the chat window please let TexTools transform
		the text."""

	def newMsg(userName, text, time=time.time()):
		# Adds Name and Time to a given message
		msg = ""
		msg += TextTools.getTime(time)
		msg += " | "
		msg += userName
		msg += ":\r\n"
		msg += text
		msg += "\r\n"

		return msg

	def getTime(time):
		# Bring the timestamp to the right format
		date = datetime.datetime.fromtimestamp(int(time)).strftime('%H:%M')
		return date



if __name__ == '__main__':

	text = TextTools.newMsg('Hans',"Hallo wie geht's dir?")
	print(text)
