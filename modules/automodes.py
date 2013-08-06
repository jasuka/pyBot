import re
import os

def automodes (self):
	if len(self.msg) >= 5:
		if self.msg[4].strip() == "add":
			addautomode(self)
			
	else:
		self.send_chan("Usage: !automodes add <nick> <flag>")



def addautomode (self):
	if self.get_host() in self.config["opers"]:
		nick = self.msg[5].strip()
		modes = self.msg[6].strip()
		chan = self.msg[2].strip()
		file = "modules/data/automodes.txt"
	
		if modes == "ao":
			## If the nick is in the file, loop through it and replace the line containing the nick
			## with the new city. We write the whole new file to temp.txt and then move it back to fmi_nicks.txt
			try:
				#f = open(file)
				if re.search("\\b"+nick+":\\b", open(file).read(), flags=re.IGNORECASE):
					with open("modules/data/temp1.txt", "w", encoding="UTF-8") as temp:
						for line in open(file):				
							str = "{0}:{1}:{2}".format(nick,modes,chan)
							temp.write(re.sub("^{0}:.*$".format(nick), str, line))
						os.remove("modules/data/automodes.txt")
						os.rename("modules/data/temp1.txt", file)
					self.send_chan("Automode ({0}) added for {1} on channel {2}".format(modes,nick,chan))
					return(True)
				## If the nick doesn't exist in the file, append it in there
				else:
					with open(file, "a", encoding="UTF-8") as file:
						str = "\r\n{0}:{1}:{2}".format(nick,modes,chan)
						file.write(str)
					self.send_chan("Automode ({0}) added for {1} on channel {2}".format(modes,nick,chan))
					return(True)
			except Exception as e:
				if self.config["debug"] == "true":
					print(e)
		else:
			self.send_chan("Currently the only user flag is 'ao'")
	else:
		self.send_chan("Unauthorized command")

