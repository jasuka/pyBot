#seendb version 1
import re, time, os
import sys_error_log

def seendb ( self ):

	if os.path.exists(self.config["log-path"]) == True: #Checking if log-path in config is valid and exists (path is generated in logger_daemon.py)
		
		if len(self.msg) >= 4:	#Recording only if server sends more than 5 parameters (0,1,2,3,4,5) etc...
			if self.msg[1] in self.irc_codes and "NOTICE" in self.msg[1]:	#do nothing if server sends any of these parameters
				return
			else:
				try:
					seendb = self.config["log-path"]+"seen.db"
					temp = self.config["log-path"]+"temp.db"
					timestamp = int(time.time())
					nick = self.get_nick()
					usertxt = ""

					for i in range(3, len(self.msg)):
						usertxt += "{0} ".format(self.msg[i])

					usertxt = re.sub(r'\\n|\\r|\\t','', usertxt)
					
					#Create the seen.db if it doesn't exist
					if not os.path.exists(seendb):
						open(seendb, 'w').close()
						self.errormsg = "[NOTICE]-[seendb] Creating database file for seendb"
						sys_error_log.log( self )
					else:
						if nick in open(seendb).read():
							with open(temp, "w", encoding="UTF-8") as tempdb:
								for line in open(seendb):				
									str = "{0}|:|{1}|:|{2}".format(nick,timestamp,usertxt[1:].strip())
									tempdb.write(re.sub("^{0}\\|\\:\\|.*$".format(nick), str.strip(), line))
									tempdb.flush()
								os.remove(seendb)
								os.rename(temp, seendb)
							return(True)
						## If the nick doesn't exist in the file, append it in there
						else:
							with open(seendb, "a", encoding="UTF-8") as file:
								str = "{0}|:|{1}|:|{2}".format(nick,timestamp,usertxt[1:])
								file.write(str)
							return(True)
				except Exception as e:
					self.errormsg = "[ERROR]-[seendb] seendb() stating: {0}".format(e)
					sys_error_log.log( self ) ## LOG the error
					if self.config["debug"] == "true":
						print(self.errormsg)	
