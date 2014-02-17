## userOutput versio 1

"""
Known issues:

*	If user has got +v while got +o and gets deopped, 
 	it doesnt remember the previous mode and sets zero prefix

*	Names list is not channel specific yet :(	

*	The bot cannot "see" itself, so bot given modes arent included

"""

import time
import sysErrorLog

def show( self ):
	
	timeStamp = "{0}".format(time.strftime("%H:%M"))
	prefix = []
	currentPrefix = ""
	
	## Parse the list from NAMES command
	if "353" in self.msg and self.listNames:
		#Format the nick list
		del self.nickList[0:len(self.nickList)]
		for i in range(5, len(self.msg)):
			if "\r\n" in self.msg[i]:
				lastNick = self.msg[i].split("\r\n")
				self.nickList.append(lastNick[0])
				return
			else:
				self.nickList.append(self.msg[i].strip(":"))
	
	#print(self.msg)

	try:
		if self.msg[1] == "MODE":
			user = self.msg[4].rstrip("\r\n")

			if self.msg[3] == "+o":

				findUser = "+{0}".format(user)

				if user in self.nickList:
					index = self.nickList.index(user)
					self.nickList[index] = "@{0}".format(user)
				elif findUser in self.nickList:
					index = self.nickList.index(findUser)
					self.nickList[index] = "@{0}".format(user)

			elif self.msg[3] == "-o":

				findUser = "@{0}".format(user)

				if findUser in self.nickList:
					index = self.nickList.index(findUser)
					self.nickList[index] = user

			elif self.msg[3] == "+v":

				findUser = "@{0}".format(user)

				if user in self.nickList:
					index = self.nickList.index(user)
					self.nickList[index] = "+{0}".format(user)
				elif findUser in self.nickList:
					index = self.nickList.index(findUser)
					self.nickList[index] = "+{0}".format(user)

			elif self.msg[3] == "-v":

				findUser = "+{0}".format(user)

				if findUser in self.nickList:
					index = self.nickList.index(findUser)
					self.nickList[index] = user

		elif self.msg[1] == "NICK":
			newNick = self.msg[2][1:].rstrip("\r\n")
			oldNick = self.get_nick()

			if oldNick in self.nickList:
				index = self.nickList.index(oldNick)
				self.nickList[index] = newNick
				
			elif "+"+oldNick  in self.nickList:
				index = self.nickList.index("+"+oldNick)
				self.nickList[index] = "+"+newNick	

			elif "@"+oldNick in self.nickList:
				index = self.nickList.index("@"+oldNick)
				self.nickList[index] = "@"+newNick

		elif self.msg[1] == "JOIN":
			self.nickList.append(self.get_nick())

		prefix = [i for i in self.nickList if self.get_nick() in i]
		prefixedNick = prefix[0]

	except Exception as e:
		#errorlgger here
		pass




	try:
		## Checking if MODE is present
		if self.msg[1] == "MODE":
			modeFound = True
		else:
			modeFound = False

		## Checking if the channel is present
		if self.msg[2][0] == "#":
			chanVerified = True
			chan = self.msg[2].rstrip("\r\n")
		else:
			chanVerified = False

		if modeFound and chanVerified:
			print("{0} [{1}] MODE ({2} {3}) by {4}".format(
				timeStamp, chan, self.msg[3], self.msg[4].rstrip("\r\n"), self.get_nick()))

		if chanVerified and not modeFound:
			rawText = []
			for i in range(3, len(self.msg)):
				rawText.append(self.msg[i].rstrip("\r\n"))

			text = ""
			for x in range(0, len(rawText)):
				text += "%s " % (rawText[x])
			
			text = text[1:]

			print("{0} [{1}] <{2}> {3}".format(
				timeStamp,chan, prefixedNick, text))
			
	except IndexError:
		#error logger ?
		pass

