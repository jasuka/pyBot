import re, time, os
def seendb ( self ):
	
	irc_codes = ["001", "002", "003", "004", "005", "042", "251", "250", "252", "254", 
				"255", "265", "266", "375", "372", "376", "433"]

	if os.path.exists(self.config["log-path"]) == True: #Checking if log-path in config is valid and exists (path is generated in logger_daemon.py)
		
		if len(self.msg) >= 4:
			if self.msg[1] in irc_codes:
				return
			else:
				try:
					seendb = self.config["log-path"]+"seen.db"
					temp = self.config["log-path"]+"temp.db"
					timestamp = int(time.time())
					nick = self.get_nick()
					usertxt = ""

					for i in range(3, len(self.msg)):
						usertxt += self.msg[i] +" "

					if nick in open(seendb).read():
						with open(temp, "w", encoding="UTF-8") as tempdb:
							for line in open(seendb):				
								str = "{0}:{1}".format(nick,timestamp)
								tempdb.write(re.sub("^{0}:.*$".format(nick), str, line))
								tempdb.flush()
							os.remove(seendb)
							os.rename(temp, seendb)
						return(True)
					## If the nick doesn't exist in the file, append it in there
					else:
						with open(seendb, "a", encoding="UTF-8") as file:
							str = "\r\n{0}:{1}".format(nick,timestamp)
							file.write(str)
						return(True)
				except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
					open(seendb, "a").close()
					if self.config["debug"] == "true":
						print("Creating file")
				except Exception as e:
					if self.config["debug"] == "true":
						print(e)
