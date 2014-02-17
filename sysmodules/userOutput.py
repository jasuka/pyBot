## userOutput versio 1
## Implemented for version 1.1 of pybot

"""
Known issues:

*	If user has got +v while got +o and gets deopped, 
 	it doesnt remember the previous mode and sets zero prefix

*	Names list is not channel specific yet :(	

*	The bot cannot "see" itself, so bot given modes arent included to prefix
	Not too sure about this one, sometimes it seems to be working just fine...

*	If someone parts the channel, it cannot get the nick prefix straight...
	We are using there self.get_nick() to have just any nick in place

"""

import time
import sysErrorLog

def nicklList ( self ):
	print("[CREATING NAMES LIST]")
	nickList = []

	if "353" in self.msg and self.listNames:
		##
		## Parse and create a nicklist
		##
		try:
			index = self.msg.index("353")
			for i in range(index+4, len(self.msg)):
				if "\r\n" in self.msg[i]:
					lastNick = self.msg[i].split("\r\n")
					nickList.append(lastNick[0])
					return
				else:
					nickList.append(self.msg[i].strip(":"))
		except Exception as e:
			## We dont bother to user if self.config["debug"] is on or not..
			## obviously it's OFF at this poinst
			self.errormsg = "[ERROR]-[userOutput] nickList() stating: {0}".format(e)
			sysErrorLog.log ( self )
		finally:
			return(nickList)

def getNickFromNicklist( self ):	
	##
	## Do we really need to import nicks from nickList into preprefixing
	## just feels like it's not needed... ( ? )
	##
	if self.activeOnchan:
		try:
			try:
				if not self.donePrefixing:
					for i in self.nickList:
						self.prePrefix.append(i)
						self.donePrefixing = True
			except Exception as e:
				## We dont bother to user if self.config["debug"] is on or not..
				## obviously it's OFF at this poinst
				self.errormsg = "[ERROR]-[userOutput] getNickFromNicklist() stating: {0}".format(e)
				sysErrorLog.log ( self )

			## Checking prefixes according to MODE events
			if self.msg[1] == "MODE":
				user = self.msg[4].rstrip("\r\n")

				if self.msg[3] == "+o":

					findUser = "{0}".format(user)

					if user in self.prePrefix:
						index = self.prePrefix.index(user)
						self.prePrefix[index] = "@{0}".format(user)

					elif findUser in self.prePrefix:
						index = self.prePrefix.index(findUser)
						self.prePrefix[index] = "@{0}".format(user)

				elif self.msg[3] == "-o":

					findUser = "@{0}".format(user)

					if findUser in self.prePrefix:
						index = self.prePrefix.index(findUser)
						self.prePrefix[index] = user

				elif self.msg[3] == "+v":

					findUser = "@{0}".format(user)

					if user in self.prePrefix:
						index = self.prePrefix.index(user)
						self.prePrefix[index] = "+{0}".format(user)
					elif findUser in self.prePrefix:
						index = self.prePrefix.index(findUser)
						self.prePrefix[index] = "+{0}".format(user)

				elif self.msg[3] == "-v":

					findUser = "+{0}".format(user)

					if findUser in self.prePrefix:
						index = self.prePrefix.index(findUser)
						self.prePrefix[index] = user

			## Checking that prefix follows with a new nick
			elif self.msg[1] == "NICK":
				newNick = self.msg[2][1:].rstrip("\r\n")
				oldNick = self.get_nick()

				if oldNick in self.prePrefix:
					index = self.prePrefix.index(oldNick)
					self.prePrefix[index] = newNick
					
				elif "+"+oldNick  in self.prePrefix:
					index = self.prePrefix.index("+"+oldNick)
					self.prePrefix[index] = "+"+newNick	

				elif "@"+oldNick in self.prePrefix:
					index = self.prePrefix.index("@"+oldNick)
					self.prePrefix[index] = "@"+newNick

			elif self.msg[1] == "JOIN":
				self.prePrefix.append(self.get_nick())

			## On PART / QUIT we want to remove user from the nicklist
			elif self.msg[1] == "PART":
				if self.get_nick()	in self.prePrefix:
					index = self.prePrefix.index(self.get_nick())
					del self.prePrefix[index]

				elif "@"+self.get_nick() in self.prePrefix:
					index = self.prePrefix.index("@"+self.get_nick())
					del self.prePrefix[index]
			
				elif "+"+self.get_nick() in self.prePrefix:
					index = self.prePrefix.index("+"+self.get_nick())
					del self.prePrefix[index]

			elif self.msg[1] == "QUIT":
				if self.get_nick()	in self.prePrefix:
					index = self.prePrefix.index(self.get_nick())
					del self.prePrefix[index]

				elif "@"+self.get_nick() in self.prePrefix:
					index = self.prePrefix.index("@"+self.get_nick())
					del self.prePrefix[index]
			
				elif "+"+self.get_nick() in self.prePrefix:
					index = self.prePrefix.index("+"+self.get_nick())
					del self.prePrefix[index]	

			## Lets parse the nick with a prefix and return it to core
			prefix = []
			prefix = [i for i in self.prePrefix if self.get_nick() in i]

			try:
				prefixedNick = prefix[0]
			except Exception as e:
				prefixedNick = self.get_nick()

			return(prefixedNick)
		except Exception as e:
			## PASS this exception
			## otherwise 'in <string>' requires string as left operand, not NoneType
			pass	



def show( self, nick ):
	timeStamp = "{0}".format(time.strftime("%H:%M"))

	if self.activeOnchan:
		try:
			
			## Checking if MODE is present
			if self.msg[1] == "MODE":
				modeFound = True
			else:
				modeFound = False

			## Checking if the channel is present
			if self.msg[2].lstrip(":").rstrip("\r\n")[0] == "#":
				chanVerified = True
				bot = False
			elif self.msg[1].lstrip(":").rstrip("\r\n")[0] == "#":
				chanVerified = True
				bot = True
			else:
				chanVerified = False

			if chanVerified:
				chan = self.msg[2].lstrip(":").rstrip("\r\n")


			listOfevents = ["QUIT", "PART", "JOIN"]
			if self.msg[1] in listOfevents and chanVerified:
				
				if self.msg[1] == "JOIN":
					print("{0} *** {1} ({3}) JOINS {2}".format(timeStamp, self.get_nick(), chan, self.get_host()))
				elif self.msg[1] == "PART":
					print("{0} *** {1} ({3}) PARTS {2}".format(timeStamp, self.get_nick(), chan, self.get_host()))
				elif self.msg[1] == "QUIT":
					print("{0} *** {1} ({2}) has quit irc".format(timeStamp, self.get_nick(), self.get_host()))
					## Something's matter with this line o_O... otherwise pretty cool


			## If the even is MODE , we don't want to show it as other stuff
			if modeFound and chanVerified:
				print("{0} [{1}] MODE ({2} {3}) by {4}".format(
					timeStamp, chan, self.msg[3], self.msg[4].rstrip("\r\n"), self.get_nick()))

			if chanVerified and not modeFound and self.msg[1] not in listOfevents:
				rawText = []
				if not bot:
					for i in range(3, len(self.msg)):
						rawText.append(self.msg[i].rstrip("\r\n"))
				else:
					for i in range(2, len(self.msg)):
						rawText.append(self.msg[i].rstrip("\r\n"))

				text = ""
				for x in range(0, len(rawText)):
					text += "%s " % (rawText[x])
				
				text = text[1:]

				print("{0} [{1}] <{2}> {3}".format(
					timeStamp,chan, nick, text))
				
		except Exception as e:
			## We dont bother to user if self.config["debug"] is on or not..
			## obviously it's OFF at this poinst
			self.errormsg = "[ERROR]-[userOutput] show() stating: {0}".format(e)
			sysErrorLog.log ( self )
			pass

