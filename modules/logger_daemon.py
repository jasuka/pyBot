##Logger daemon version 0.1 

from time import gmtime, strftime

def logger_daemon ( self ):

	if "353" in self.msg or "366" in self.msg or "412" in self.msg:
		return
	else:
		chan = self.msg[2]
		brackets = self.config["TimestampBrackets"].split(",")
		usertxt = ""

		for i in range(3, len(self.msg)):
			usertxt += self.msg[i] +" "
	try:
		if chan[0] == "#":
			log = "logs/"+chan+".log"
			logline = brackets[0]+strftime(self.config["timeformat"])+brackets[1] + " " + self.get_nick() + " @ " + chan + " " + usertxt

			with open(log, "a") as log:
				log.write(logline)
				log.flush()
	except TypeError as msg:
		if self.config["debug"] == "true":
			print(msg)

