##Logger daemon version 0.1 
def logger_daemon ( self ):
	log = "logs/logger.log"
	usertxt = ""

	for i in range(3, len(self.msg)):
		usertxt += self.msg[i] +" "

	logline = self.get_nick()+ " @ " + self.msg[2] + " " + usertxt

	with open(log, "a") as log:
		log.write(logline)
		log.flush()	
	
