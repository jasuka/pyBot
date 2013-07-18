##Logger daemon version 0.2.1

from time import gmtime, strftime
import os

def logger_daemon ( self ):
	if os.path.exists(self.config["log-path"]) == True:
	
		try:
			chan = self.msg[2]
		except IndexError:
			print("Error, cannot log\r\n")
		else:

			if "353" in self.msg or "366" in self.msg or "412" in self.msg:
				return
			else:
				brackets = self.config["TimestampBrackets"].split(",")
				usertxt = ""

				for i in range(3, len(self.msg)):
					usertxt += self.msg[i] +" "
			try:
				if chan[0] == "#":
					log = self.config["log-path"]+chan+".log"
					logline = brackets[0]+strftime(self.config["timeformat"])+brackets[1] + " " + self.get_nick() + " @ " + chan + " " + usertxt

					with open(log, "a") as log:
						log.write(logline)
						log.flush()
			except TypeError as msg:
				if self.config["debug"] == "true":
					print(msg)
	else:
		print("Cannot find existing folder for logs, creating: "+self.config["log-path"])
		os.mkdir(self.config["log-path"])

