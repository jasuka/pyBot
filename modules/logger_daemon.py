
def logger_daemon ( self ):
	log = "logs/logger.log"
	logline = self.get_nick()
	with open(log, "a") as log:
		log.write(logline)
		log.flush()	
	
