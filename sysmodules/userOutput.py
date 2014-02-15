## userOutput versio 1

import time
import sysErrorLog

def show( self ):
	
	timeStamp = "{0}".format(time.strftime("%H:%M"))
	prefix = []
	
	## NICK LISTING
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
	
	#print(self.nickList)

	try:
		prefix = [i for i in self.nickList if self.get_nick() in i]
		prefix = prefix[0]
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
				timeStamp,chan, prefix, text))
			
	except IndexError:
		#error logger ?
		pass

