import urllib.request
import os
import re
import time
## Get HTML for given url
def getHtml( self, url, useragent):
	try:
		if useragent == True:
			user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
			headers = { 'User-Agent' : user_agent }
			req = urllib.request.Request(url, None, headers)
		else:
			req = urllib.request.Request(url, None)
			
		html = urllib.request.urlopen(req, timeout = 20).read()
		return(html)
	except Exception as e:
		self.send_chan( "~ {0} ({1})".format(e, url) )
## End

## Check if the city exists in Finland
def checkCity ( city ):

	try:
		city = city.title().strip()
		with open("modules/data/cities.txt", "r", encoding="UTF-8") as file:
			data = [x.strip() for x in file.readlines()]

		if city in data:
			return(True)
	except IOError as e:
		if self.config["debug"] == "true":
			print(e)
## End

## Clears html tags from a string
def delHtml( html ):
	try:
		html = re.sub('<[^<]+?>', '', html)
		return(html)
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)
			
## End

## Automodes checkup on event JOIN
def modecheck (self):
	file = "modules/data/automodes.txt"
	try:
		with open(file, "r", encoding="UTF-8") as modes:
			for line in modes:
				if re.search("\\b"+self.get_host()+":\\b", line, flags=re.IGNORECASE):
					spl = line.split(":")
					#print(spl[0]+" "+spl[1])
					if spl[1].strip() == "ao":
						self.send_data("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
						print("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
	except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
		open(file, "a").close()
		if self.config["debug"] == "true":
			print("Creating file for automodes '{0}'".format(file))

## End

## ADD AUTOMODE
def addautomode (self,modes,chan):
	
	identhost = self.hostident.strip() 	#this is created by getRemoteHost() down below which is later on called
					   	#in core as a bot wide variable when server sends whoise code 311
	file = "modules/data/automodes.txt"

	if modes == "ao":
		try:
			if re.search("\\b"+identhost+":\\b", open(file).read(), flags=re.IGNORECASE):
				with open("modules/data/temp1.txt", "w", encoding="UTF-8") as temp:
					for line in open(file):				
						str = "{0}:{1}:{2}".format(identhost,modes,chan)
						temp.write(re.sub("^{0}:.*$".format(identhost), str, line))
					os.remove("modules/data/automodes.txt")
					os.rename("modules/data/temp1.txt", file)
				self.send_data("PRIVMSG {2} :Automode ({0}) changed for {1} on channel {2}".format(modes,identhost,chan))
				return(True)
			## If the nick doesn't exist in the file, append it in there
			else:
				with open(file, "a", encoding="UTF-8") as file:
					str = "\r\n{0}:{1}:{2}".format(identhost,modes,chan)
					file.write(str)
				self.send_data("PRIVMSG {2} :Automode ({0}) added for {1} on channel {2}".format(modes,identhost,chan))
				return(True)

		except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
			open(file, "a").close()
			if self.config["debug"] == "true":
				print("Creating file for automodes '{0}'".format(file))
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)
	else:
		self.send_data("PRIVMSG {0} :Currently the only user flag is 'ao'".format(chan))
## END

## Return remote host based on given nick

def getRemoteHost (self):
	#print("{0}@{1}".format(self.msg[4],self.msg[5]))
	hostident = "{0}@{1}".format(self.msg[4],self.msg[5])
	return(hostident)
## End
