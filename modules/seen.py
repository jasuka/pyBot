import time, datetime
from time import gmtime, strftime
import re

def seen ( self ):
	
	if self.config["logging"] == True:
		if len(self.msg) >= 5:
			try:
				seendb = self.config["log-path"]+"seen.db"
				with open(seendb): pass
			except Exception as e:
				if self.config["debug"] == "true":
					print(e)
			else:
				nick = self.msg[4].rstrip("\r\n")
				with open(seendb, "r", encoding="UTF-8") as db:
					for line in db:
						if nick in line:
							spl = line.split(";")
							name = spl[0]
							dbtime = spl[1].rstrip("\r\n")
							dbconvert = datetime.datetime.fromtimestamp(int(dbtime)).strftime('[%d.%m.%Y] %H:%M:%S')
							self.send_chan(name+" spoke last time: "+dbconvert)
		else:
			self.send_chan("Usage: !seen <nick>")
	else:
		self.send_chan("Logging must be enabled from config in order to use this module")
					
