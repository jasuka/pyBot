import sysErrorLog
from random import shuffle
from random import randint
class Cache:
	winningPool = 10

def game( self ):

	gameObjects = [0,1,2,3,4]
	shuffle(gameObjects) 
	spinnerOne = gameObjects[randint(0,4)]
	shuffle(gameObjects)
	spinnerTwo = gameObjects[randint(0,4)]
	shuffle(gameObjects)
	spinnerThree = gameObjects[randint(0,4)]
	
	if (Cache.winningPool == 0):
		self.send_chan("Kassasi on tyhjä, et voi pelata :(")
	else:
		if (((spinnerOne + 1) == spinnerTwo) and (spinnerTwo + 1) == spinnerThree):
			Cache.winningPool += 5
			self.send_chan("[{0}] [{1}] [{2}], Kolmen suora, kassassa on on nyt {3} dogecoinia".format(spinnerOne,spinnerTwo,spinnerThree,Cache.winningPool))

		elif ((spinnerOne == spinnerTwo) and (spinnerOne == spinnerThree)):
			Cache.winningPool += 3
			self.send_chan("[{0}] [{1}] [{2}], Kolme samaa, kassassa on on nyt {3} dogecoinia".format(spinnerOne,spinnerTwo,spinnerThree,Cache.winningPool))

		elif ((spinnerOne == spinnerTwo) or (spinnerTwo == spinnerThree) or (spinnerOne == spinnerThree)):
			Cache.winningPool += 2
			self.send_chan("[{0}] [{1}] [{2}], Kaksi samaa, kassassa on nyt {3} dogecoinia".format(spinnerOne,spinnerTwo,spinnerThree,Cache.winningPool))
		
		else:
			Cache.winningPool -= 1
			self.send_chan("[{0}] [{1}] [{2}], Ei voittoa :( Kassassa on {3} dogecoinia jäljellä".format(spinnerOne,spinnerTwo,spinnerThree,Cache.winningPool))

