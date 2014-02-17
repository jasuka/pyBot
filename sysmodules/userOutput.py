## userOutput versio 1

"""
Known issues:

*	If user has got +v while got +o and gets deopped, 
 	it doesnt remember the previous mode and sets zero prefix

*	Names list is not channel specific yet :(	

*	The bot cannot "see" itself, so bot given modes arent included to prefix

* 	Error handling and logging is still absent

*	'list out of range' on PART, QUIT doesn't clear the nicklist

*	If someone parts the channel, it cannot get the nick prefix straight...
	We are using there self.get_nick() to have just any nick in place

"""

import time
import sysErrorLog

def nicklList ( self ):
	print("[CREATING NAMES LIST]")
	nickList = []
	#print(self.msg)
	## Parse the list from NAMES command
	if "353" in self.msg and self.listNames:

		#Format the nick list and create new list
		#del nickList[0:len(nickList)]
		try:
			index = self.msg.index("353")
			for i in range(index+4, len(self.msg)):
				if "\r\n" in self.msg[i]:
					lastNick = self.msg[i].split("\r\n")
					nickList.append(lastNick[0])
					#print(lastNick[0])
					return
				else:
					#print(self.msg[i].strip(":"))
					nickList.append(self.msg[i].strip(":"))
		except Exception as e:
			print(e)
		finally:
			return(nickList)

def getNickFromNicklist( self ):	
	
	if self.activeOnchan:
		try:
			try:
				if not self.donePrefixing:
					for i in self.nickList:
						self.prePrefix.append(i)
						self.donePrefixing = True
				else:
					del self.prefix[0:len(self.prefix)]
					for i in self.prefix:
						self.prePrefix.append(i)

			except Exception as e:
				print(e)
			
			if self.msg[1] == "MODE":
				user = self.msg[4].rstrip("\r\n")
				#print(self.msg) ##  DEBUG

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

			self.prefix = [i for i in self.prePrefix if self.get_nick() in i]
			try:
				prefixedNick = self.prefix[0]
				#return(prefixedNick)
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
			if self.msg[2][0] == "#":
				chanVerified = True
				bot = False
			elif self.msg[1][0] == "#":
				chanVerified = True
				bot = True
			else:
				chanVerified = False

			if chanVerified:
				chan = self.msg[2].rstrip("\r\n")

			if modeFound and chanVerified:
				print("{0} [{1}] MODE ({2} {3}) by {4}".format(
					timeStamp, chan, self.msg[3], self.msg[4].rstrip("\r\n"), self.get_nick()))

			if chanVerified and not modeFound:
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
				
		except IndexError:
			#error logger ?
			pass

