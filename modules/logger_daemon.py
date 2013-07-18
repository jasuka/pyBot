##Logger daemon version 1

from time import gmtime, strftime
import os

def logger_daemon ( self ):
	if os.path.exists(self.config["log-path"]) == True:
	
		if len(self.msg) >= 4:

			if "353" in self.msg or "366" in self.msg or "412" in self.msg:
				return
			else:
				brackets = self.config["TimestampBrackets"].split(",")
				usertxt = ""
				chan = self.msg[2]

				for i in range(3, len(self.msg)):
					usertxt += self.msg[i] +" "
			#try: 	will cleanup these commented lines later, for now it seems these are not needed
				if chan[0] == "#":
					log = self.config["log-path"]+chan+".log"
					logline = brackets[0]+strftime(self.config["timeformat"])+brackets[1] + " " + self.get_nick() + " @ " + chan + " " + usertxt

					with open(log, "a") as log:
						log.write(logline)
						log.flush()
			#except TypeError as msg:
				#if self.config["debug"] == "true":
					#print(msg)

	else:
		print("Cannot find existing folder for logs, creating: "+self.config["log-path"])
		os.mkdir(self.config["log-path"])

