##Logger daemon version 0.1 

from time import gmtime, strftime
import re

def logger_daemon ( self ):
	
	nick = ""
	try:
		nick = re.search(":({0})!".format(self.get_nick()), self.msg[0]).group(1)
	except:
		raise
		
	if  nick.strip() != self.config["nick"] and len(nick) > 0:
		log = "logs/logger.log"
		usertxt = ""

		for i in range(3, len(self.msg)):
			usertxt += self.msg[i] +" "

		timestamp = "["+strftime("%H:%M:%S")+"]"
		logline = timestamp + " " + self.get_nick() + " @ " + self.msg[2] + " " + usertxt

		with open(log, "a") as log:
			log.write(logline)
			log.flush()
	else:
		return	

