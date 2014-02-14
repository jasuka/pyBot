## userOutput versio 1

import time

def show( self ):

	timeStamp = "[{0}]".format(time.strftime("%d.%m.%Y/%H:%M:%S"))
	try:

		## parsing events ONLY if there is a channel present
		if self.msg[2][0] == "#":
			chanVerified = True
			chan = self.msg[2]
		else:
			chanVerified = False

		if self.msg[1] == "MODE" and chanVerified:
			chanMode = True
			print("{0} MODE {1} [{2} {3}] by {5}".format(
				timeStamp, chan, self.msg[3], self.msg[4], self.get_nick()))
		else:
			chanMode = False

		if chanVerified and not chanMode:
			rawText = []
			for i in range(3, len(self.msg)):
				rawText.append(self.msg[i].rstrip("\r\n"))

			text = ""
			for x in range(0, len(rawText)):
				text += "%s " % (rawText[x])
			
			text = text[1:]

			print("{0} ({1}) {2} >> {3}".format(
				timeStamp,chan, self.get_nick(), text))
	
	except IndexError:
		pass