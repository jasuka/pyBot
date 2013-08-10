
def getHost (self):
	
	nick = self.msg[4].strip()
	whois = self.send_data("WHOIS {0}".format(nick))
	
	
