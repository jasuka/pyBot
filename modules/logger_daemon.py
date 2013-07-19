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

		
	
	if os.path.exists(self.config["log-path"]) == True:
		seendb = self.config["log-path"]+"seendb.txt"
		timeformat = strftime(self.config["timeformat"])

		try:
			if self.get_nick() in open(seendb).read():
				with open(seendb, "w", encoding="UTF-8") as temp:
					for line in open(seendb):				
						str = "{0}:{1}".format(timeformat,self.get_nick())
						temp.write(re.sub("^{0}:.*$".format(self.get_nick()), str, line))
					os.remove(seendb)
					os.rename(self.config["log-path"]+"temp.txt", seendb)
					temp.close()
				return(True)
			## If the nick doesn't exist in the file, append it in there
			else:
				with open(seendb, "a", encoding="UTF-8") as file:
					str = "\r\n{0}:{1}".format(timeformat,self.get_nick())
					file.write(str)
					file.close()
				return(True)
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)
				print("Creating file")
				with open(seendb, "a") as db:
					db.close()
				
	 

