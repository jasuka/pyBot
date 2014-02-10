##Error logger

from time import gmtime, strftime
import time
import os
import re
from traceback import format_exc

def log ( self ):

	if os.path.exists(self.config["log-path"]) == True:	#Checking if log-path in config is valid and exists

		brackets = self.config["TimestampBrackets"].split(",") #Looking brackets from the config file

		log = self.config["log-path"]+"error.log"
		logline = "{0}{1}{2} {3}. {4}\r\n".format( ## 0-2 timestamp, 3 error message
						brackets[0], strftime(self.config["timeformat"]), brackets[1], self.errormsg, format_exc())

		with open(log, "a") as logi: #Opening the log and appending the latest result
			logi.write(logline)
			logi.flush()


	else:
		try:
			if self.config["debug"] == True: #If the path set in config doesn't exist, create one
				print("Cannot find existing folder for logs, creating: {0}".format(self.config["log-path"]))
			os.mkdir(self.config["log-path"])
		except Exception as e:
			if self.config["debug"] == True:
				print("[ERROR]-[sysErrorLog] log() stating: {0}, Plus that im a retard, and i cant log my own errors :((".format(e))
	


