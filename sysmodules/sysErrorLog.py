##Error logger version 2

from time import gmtime, strftime
import time
import os
import re
from traceback import format_exc

def log ( self ):

	if os.path.exists(self.config["log-path"]):	#Checking if log-path in config is valid and exists

		try:
			brackets = self.config["TimestampBrackets"].split(",") #Looking brackets from the config file

			log = self.config["log-path"]+"error.log"

			if self.config["errLoglevel"] != 0:
				if self.config["errLoglevel"] == 1: ## this level records only the error
					logline = "{0}{1}{2} {3}.".format( ## 0-2 timestamp, 3 error message
									brackets[0], strftime(self.config["timeformat"]), brackets[1], self.errormsg)

				elif self.config["errLoglevel"] == 2: ## error with a backtrace
					try:
						traceback = format_exc()
					except AttributeError:
						traceback = "Backtrace not available"
					logline = "{0}{1}{2} {3}.\r\n{4}\r\n".format( ## 0-2 timestamp, 3 error message
									brackets[0], strftime(self.config["timeformat"]), brackets[1], self.errormsg, traceback)	
													
				with open(log, "a") as logi: #Opening the log and appending the latest result
					logi.write(logline)
					logi.flush()

		except Exception as e:
			print("{0}[ERROR]-[sysErrorLog] log()(1) stating: {1}, Plus that im a retard, and i cant log my own errors :(({2}".format(self.color("red"),e,self.color("end")))

	else:
		try:
			if self.config["debug"]: #If the path set in config doesn't exist, create one
				print("{0}[NOTICE]-[sysErrorLog] Cannot find existing folder for logs, creating: {1}{2}".format(self.color("blue"),self.config["log-path"]),self.color("end"))
			os.mkdir(self.config["log-path"])
		except Exception as e:
			if self.config["debug"]:
				print("{0}[ERROR]-[sysErrorLog] log()(2) stating: {1}, Plus that im a retard, and i cant log my own errors :(({2}".format(self.color("red"),e,self.color("end")))
	


