## tPlayer = tennis player who will belong to fPlayers##

import constants

class tPlayer:

	def __init__(self, name, sex, attribute):
		self.name = name
		self.sex = sex
		self.attribute = int(attribute)
		self.points = 0
		self.alive = 1
		self.history = list()


## fPlayer = fantasy player##

class fPlayer:

	def __init__(self, name):
		self.name = name
		self.total = 0
		self.team = list()
		self.bench = list()

	def addPickUp(self, name, sex, attribute):

		self.bench.append(tPlayer(name, sex, attribute))

		daysOfPlay = 7

		#setting up some dummy data so it doesn't crash when printing the data
		for day in range(0, daysOfPlay):

			self.bench[-1].history.append((constants.DATES_2019_AUS[day],'-'))

