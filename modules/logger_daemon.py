##Logger daemon version 0.1 

from time import gmtime, strftime

def logger_daemon ( self ):

	if "353" in self.msg or "366" in self.msg or "412" in self.msg:
		return
	else:
		brackets = self.config["TimestampBrackets"].split(",")
		log = "logs/logger.log"
		usertxt = ""

		for i in range(3, len(self.msg)):
			usertxt += self.msg[i] +" "
	try:
		logline = brackets[0]+strftime(self.config["timeformat"])+brackets[1] + " " + self.get_nick() + " @ " + self.msg[2] + " " + usertxt

		with open(log, "a") as log:
			log.write(logline)
			log.flush()
	except TypeError as msg:
		if self.config["debug"] == "true":
			print(msg)

