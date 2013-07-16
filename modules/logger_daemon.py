##Logger daemon version 0.1 

from time import gmtime, strftime
import re

def logger_daemon ( self ):

	if "353" in self.msg or "366" in self.msg:
		return
	else:
		log = "logs/logger.log"
		usertxt = ""

		for i in range(3, len(self.msg)):
			usertxt += self.msg[i] +" "

		logline = "["+strftime(self.config["timestamp"])+"]" + " " + self.get_nick() + " @ " + self.msg[2] + " " + usertxt

		with open(log, "a") as log:
			log.write(logline)
			log.flush()
	
