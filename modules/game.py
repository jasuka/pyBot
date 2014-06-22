import sysErrorLog
from random import randint

class slotGame(object):

	class cache(object):
		winningPool = 10

	def spinWheels(self):
		self.wheelOne = randint(1,13)
		self.wheelTwo = randint(1,13)
		self.wheelThree = randint(1,13)

	def roundResults(self):
		if (gameCache.winningPool > 0):
			if (((self.wheelOne + 1) == self.wheelTwo) and (self.wheelTwo + 1) == self.wheelThree):
				gameCache.winningPool += 5
				roundResult = "[{0}] [{1}] [{2}], Kolmen suora, kassassa on on nyt {3} dogecoinia".format(self.wheelOne, self.wheelTwo, self.wheelThree, gameCache.winningPool)
				return(roundResult)
			elif ((self.wheelOne == self.wheelTwo) and (self.wheelOne == self.wheelThree)):
				gameCache.winningPool += 3
				roundResult = "[{0}] [{1}] [{2}], Kolme samaa, kassassa on on nyt {3} dogecoinia".format(self.wheelOne, self.wheelTwo, self.wheelThree, gameCache.winningPool)
				return(roundResult)
			elif ((self.wheelOne == self.wheelTwo) or (self.wheelTwo == self.wheelThree) or (self.wheelOne == self.wheelThree)):
				gameCache.winningPool += 2
				roundResult = "[{0}] [{1}] [{2}], Kaksi samaa, kassassa on nyt {3} dogecoinia".format(self.wheelOne, self.wheelTwo, self.wheelThree, gameCache.winningPool)
				return(roundResult)
			else:
				gameCache.winningPool -= 1
				roundResult = "[{0}] [{1}] [{2}], Ei voittoa :( Kassassa on {3} dogecoinia jäljellä".format(self.wheelOne, self.wheelTwo, self.wheelThree, gameCache.winningPool)
				return(roundResult)

		else:
			roundResult = "Kassasi on tyhjä, et voi pelata :("
			return(roundResult)

	

def game(self):
	slots.spinWheels()
	self.send_chan(slots.roundResults())

slots = slotGame()
gameCache = slots.cache()

