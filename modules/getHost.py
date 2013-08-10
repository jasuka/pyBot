
def getHost (self):
	
	nick = self.msg[4].strip()
	self.send_data("WHOIS {0}".format(nick))
	if "311" in self.msg:
		print("LOL")
	
	
