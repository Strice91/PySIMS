import uuid
import random

class contactList():
	def __init__(self, rawAns, username):
		self.raw = rawAns
		self.name = username
		self.List = {}
		
	def getList(self):

		for item in self.raw:
			
			item = item.split(',')
			uid = item[0].split(':')
			uid = uid[1]

			name = item[1]

			if item[2] == '1':
				status = 'online'
			else:
				status = 'offline'

			if not name == self.name:
				c = contact(uid, name, status)
				self.List[c.UID] = {'UID': c.UID, 'name': c.name, 'status': c.status}

		#print('Contacts:')
		#print(self.List)
		return self.List

	def getListRandom(self):
		cList = {}

		for x in range(0,self.raw):
			c = contactRandom()
			cList[c.UID] = {'UID': c.UID, 'name': c.name, 'status': c.status}

		return cList

class contactRandom():

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


class contact():

	def __init__(self, uid, name, status):
		self.UID = uid
		self.name = name
		self.status = status

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



		