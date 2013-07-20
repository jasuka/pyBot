##Logger daemon version 1

from time import gmtime, strftime
import time
import os
import re

def logger_daemon ( self ):

	irc_codes = ["001", "002", "003", "004", "005", "042", "251", "250", "252", "254", 
				"255", "265", "266", "375", "372", "376", "433"]

	if os.path.exists(self.config["log-path"]) == True:
	
		if len(self.msg) >= 4:

			if self.msg[1] in irc_codes:
				return
			else:
				brackets = self.config["TimestampBrackets"].split(",")
				usertxt = ""
				chan = self.msg[2]

				for i in range(3, len(self.msg)):
					usertxt += self.msg[i] +" "

				if chan[0] == "#":
					log = self.config["log-path"]+chan+".log"
					logline = brackets[0]+strftime(self.config["timeformat"])+brackets[1] + " " + self.get_nick() + " @ " + chan + " " + usertxt

					with open(log, "a") as log:
						log.write(logline)
						log.flush()


	else:
		try:
			if self.config["debug"] == "true":
				print("Cannot find existing folder for logs, creating: "+self.config["log-path"])
			os.mkdir(self.config["log-path"])
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)

		
	


