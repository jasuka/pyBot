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
				nick 		= self.msg[4].rstrip("\r\n")
				nick_in_line 	= 0
				
				
				with open(seendb, "r", encoding="UTF-8") as db:
					for line in db:
						if re.search("\\b"+nick+":\\b", line, flags=re.IGNORECASE):
							spl 		= line.split(":")
							name 		= spl[0]
							dbtime 		= spl[1].rstrip("\r\n")
							dbconvert 	= datetime.datetime.fromtimestamp(int(dbtime)).strftime('[%d.%m.%Y] %H:%M:%S')
							timediff 	= int(time.time()) - int(dbtime)
							hours 		= datetime.datetime.fromtimestamp(int(timediff)).strftime('%H')
							minutes 	= datetime.datetime.fromtimestamp(int(timediff)).strftime('%M')
							seconds 	= datetime.datetime.fromtimestamp(int(timediff)).strftime('%S')
							nick_in_line	= 1
							
				if nick_in_line == 1:
					self.send_chan(name+" spoke last time: "+dbconvert+
						" which is exactly "+hours+" hours "+minutes+" minutes "+seconds+" seconds ago.")
				else:
					self.send_chan("I have never logged "+nick+" while being on any channel")

		else:
			self.send_chan("Usage: !seen <nick>")
	else:
		self.send_chan("Logging must be enabled from config in order to use this module")
					
