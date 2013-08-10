import urllib.request
import os
import re

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

## Return remote host based on given nick

def getRemoteHost (self):
	#print("{0}@{1}".format(self.msg[4],self.msg[5]))
	hostident = "{0}@{1}".format(self.msg[4],self.msg[5])
	return(hostident)
## End

