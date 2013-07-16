
def logger_daemon ( self, data ):
	log = open("logs/logger.log", "a")
	logline = self.get_nick()
	log.write(logline)
	log.flush()	
	
