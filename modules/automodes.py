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
				with open("modules/data/automodes.txt", "r", encoding="UTF-8") as temp:
					for line in temp:				
						outti = line.split("@")
						if outti[0] == self.msg[4].strip():
							autti = outti[1].split(";")
							self.send_chan("User {0} has currently mode +{1}".format(self.msg[4].strip(),autti[1]))
				## THIS IS HORRIBLE :D so called purkkafixi..:D
						
					
				
		else:
			self.send_chan("Unauthorized command")
	else:
		self.send_chan("Usage: !automodes add <nick> <flag> ## To add a mode av or ao to the user")
		self.send_chan("Usage: !automodes <nick> ## To see modes the user has")


##							##
#							 #
# The rest of this module can be found from core/syscmd  #
#							 #
##							##
