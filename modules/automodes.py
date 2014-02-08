import re
import os
import syscmd
import time
import sqlite3

def automodes (self):
	if len(self.msg) >= 5:
		if self.msg[4].strip() == "me":
			try:
				db = sqlite3.connect("modules/data/automodes.db")
				cur = db.cursor()
				cur.execute("""SELECT mode FROM automodes WHERE identhost = ? """,(self.get_host(),))
				result = cur.fetchone()
				if result:
					self.send_chan("User {0} has currently mode +{1}".format(self.get_host(), result[0]))
				else:
					self.send_chan("Unfortunately you are not on the automodes list :(")
			except Exception as e:
				raise e
			finally:
				db.close()

		if self.msg[4].strip() == "set":
			if self.get_host() in self.config["opers"]:
				## As for a quick fix, these are made bot wide variables
				self.modes = self.msg[6].strip() 
				self.channel = self.msg[2].strip()
				## End section of system wide variables ...
				nick = self.msg[5].strip()
				self.whois(nick)
			else:
				self.send_chan("Unauthorized command")
	else:
		self.send_chan("Usage: !automodes set <nick> <flag> ## To add a mode av or ao to the user")
		self.send_chan("Usage: !automodes me ## To see modes the user has")


##							##
#							 #
# The rest of this module can be found from core/syscmd  #
#							 #
##							##
