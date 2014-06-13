import uuid
import random

class contactList():
	def __init__(self,i):
		self.amount = i
		
	def getList(self):
		cList = {}

		for x in range(0,self.amount):
			c = contact()
			cList[c.UID] = {'UID': c.UID, 'name': c.name, 'status': c.status}

		return cList



class contact():

	def __init__(self):
		self.UID = self.generateUID()
		self.name = self.getName()
		self.status = self.getStatus()

	def generateUID(self):
		return uuid.uuid4().hex

	def getStatus(self):
		status = ('online', 'offline', 'away', 'busy')
		return random.choice(status)

	def getName(self):
		names = (	'Sepp', 
					'Franz', 
					'Hans', 
					'Paul', 
					'Done', 
					'Markus', 
					'Lisa', 
					'Jojo', 
					'Martin', 
					'Daniel',
					'SuperSepp300')
		return random.choice(names)



		