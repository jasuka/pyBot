import re
import os

def automodes (self):
	if self.msg[4].strip() == "add":
		addautomode(self)



def addautomode (self):
	nick = self.msg[5]
	modes = self.msg[6] 
	file = "modules/data/automodes.txt"
	
	## If the nick is in the file, loop through it and replace the line containing the nick
	## with the new city. We write the whole new file to temp.txt and then move it back to fmi_nicks.txt
	try:
		#f = open(file)
		if re.search("\\b"+nick+":\\b", open(file).read(), flags=re.IGNORECASE):
			with open("modules/data/temp1.txt", "w", encoding="UTF-8") as temp:
				for line in open(file):				
					str = "{0}:{1}".format(nick,modes)
					temp.write(re.sub("^{0}:.*$".format(nick), str, line))
				os.remove("modules/data/automodes.txt")
				os.rename("modules/data/temp1.txt", file)
			return(True)
		## If the nick doesn't exist in the file, append it in there
		else:
			with open(file, "a", encoding="UTF-8") as file:
				str = "\r\n{0}:{1}".format(nick,modes)
				file.write(str)
			return(True)
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)
