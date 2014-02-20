##Error logger version 2

from time import gmtime, strftime
import time
import os
import re
from traceback import format_exc

def log ( self, backtrace = True):

	#Checking if log-path in config is valid and exists
	if os.path.exists(self.config["log-path"]):

		try:
			#Looking brackets from the config file
			brackets = self.config["TimestampBrackets"].split(",") 

			log = self.config["log-path"]+"error.log"

			if self.config["errLoglevel"] != 0:
				## this level records only the error
				if self.config["errLoglevel"] == 1: 
					## 0-2 timestamp, 3 error message
					logline = "{0}{1}{2} {3}.".format(
						brackets[0], strftime(self.config["timeformat"]),
							brackets[1], self.errormsg)

				## error with a backtrace			
				elif self.config["errLoglevel"] == 2: 
					if backtrace = True:
						try:
							traceback = format_exc()
						except AttributeError:
							traceback = "Backtrace not available"
						## 0-2 timestamp, 3 error message
						logline = "{0}{1}{2} {3}.\r\n{4}\r\n".format(
							brackets[0], strftime(self.config["timeformat"]),
								brackets[1], self.errormsg, traceback)
					else:
						logline = "{0}{1}{2} {3}.".format(
							brackets[0], strftime(self.config["timeformat"]),
								brackets[1], self.errormsg)


				#Opening the log and appending the latest result									
				with open(log, "a") as logi: 
					logi.write(logline)
					logi.flush()

		except Exception as e:
			print("{0}[ERROR]-[sysErrorLog] log()(1) stating: {1}, Plus that im a retard, and i cant log my own errors :(({2}"
				.format(self.color("red"),e,self.color("end")))

	else:
		try:
			if self.config["debug"]: #If the path set in config doesn't exist, create one
				print("{0}[NOTICE]-[sysErrorLog] Cannot find existing folder for logs, creating: {1}{2}"
					.format(self.color("blue"),self.config["log-path"]),self.color("end"))
			os.mkdir(self.config["log-path"])
		except Exception as e:
			if self.config["debug"]:
				print("{0}[ERROR]-[sysErrorLog] log()(2) stating: {1}, Plus that im a retard, and i cant log my own errors :(({2}"
					.format(self.color("red"),e,self.color("end")))
	


