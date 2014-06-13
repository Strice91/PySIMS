import datetime
import time

class TextTools(object):

	def newMsg(userName, text, time=time.time()):
		msg = ""
		msg += TextTools.getTime(time)
		msg += " | "
		msg += userName
		msg += ":\r\n"
		msg += text
		msg += "\r\n"

		return msg

	def getTime(time):
		date = datetime.datetime.fromtimestamp(int(time)).strftime('%H:%M')
		return date



if __name__ == '__main__':

	text = TextTools.newMsg('Hans',"Hallo wie geht's dir?")
	print(text)
