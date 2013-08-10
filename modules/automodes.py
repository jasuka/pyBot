import re
import os
import syscmd
import time

def automodes (self):
	if len(self.msg) >= 5:
		if self.get_host() in self.config["opers"]:
			if self.msg[4].strip() == "add":
				## As for a quick fix, these are made bot wide variables
				self.modes = self.msg[6].strip() 
				self.channel = self.msg[2].strip()
				## End section of system wide variables ...
				nick = self.msg[5].strip()
				self.whois(nick)
		else:
			self.send_chan("Unauthorized command")
	else:
		self.send_chan("Usage: !automodes add <nick> <flag>")


##							##
#							 #
# The rest of this module can be found from core/syscmd  #
#							 #
##							##
