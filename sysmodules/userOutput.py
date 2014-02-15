## userOutput versio 1

import time

def show( self ):

	timeStamp = "{0}".format(time.strftime("%H:%M"))
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
				timeStamp,chan, self.get_nick(), text))
			
	except IndexError:
		pass

