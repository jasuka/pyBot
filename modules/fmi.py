import urllib.parse
from bs4 import BeautifulSoup
import re
import os
import syscmd
import sys_error_log

def fmi( self ):

	## For saving the city
	if len(self.msg) == 6:
		if "set" in self.msg:
			city = self.msg[5]
			setCity( self, city )
			self.send_notice( "Your city {0} has been saved!".format(city.title().strip()))
	else:
		try:
			if len(self.msg) == 4:	## when called only with !fmi, see if the city is saved
				city = getCity( self )
				if city == None:
					city = self.msg[4]
			else:
				city = self.msg[4].strip() #With !fmi City
		except IndexError:
			self.send_chan( "Usage: !fmi <city> | !fmi set <city>" )
			raise
			
		if "set" not in city and syscmd.checkCity( self, city ): # We don't want to look for a city named "set"
			
			city = city.title().strip()
			parameter = urllib.parse.quote(city)
			url = "http://ilmatieteenlaitos.fi/saa/" + parameter
			
			if city == "Oulu":
				url = "http://ilmatieteenlaitos.fi/saa/" + parameter + "?&station=101799"
			if city == "Helsinki":
				url = "http://ilmatieteenlaitos.fi/saa/" + parameter + "?&station=100971"
			if city == "Kilpisjärvi":
				url = "http://ilmatieteenlaitos.fi/saa/enonteki%C3%B6/" + parameter
	
			html = syscmd.getHtml(self, url, True )
 
			try:
				soup = BeautifulSoup(html)
				text = ""
				## When the weather was updated
				time = soup.find_all("span", class_="time-stamp")
				time = time[0].string.split(" ")
				time = time[1][:-7]

				str = soup.findAll("span", {"class" : "parameter-name-value"})
	   
				## Loop the reusts into a string
				for a in str:
					text += "{0} - ".format(a)
	   
				## Remove the Html tags	
				trimmed = syscmd.delHtml(text)

				output = "{0} klo {1}: {2}".format(city.strip(), time, trimmed)
				self.send_chan( output )
			except Except as e:
				self.errormsg = "[ERROR]-[fmi] fmi() stating: {0}".format(e)
				sys_error_log.log( self ) ## LOG the error
				if self.config["debug"] == "true":
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			self.send_chan( "City {0} doesn't exist!".format(city.title().strip()) )
			

## Return saved city for the nick
def getCity ( self ):

	nick = self.get_nick()
	file = "modules/data/fmi_nicks.txt"
	
	try:
		with open(file, "r", encoding="UTF-8") as f:
			for line in f:
				if re.search("\\b"+nick+":\\b", line, flags=re.IGNORECASE):
					city = line.split(":")
					return(city[1])
	except (OSError, IOError): ## Create an empty fmi_nicks.txt if it doesn't exist
		self.errormsg = "[NOTICE]-[fmi] Creating fmi_nicks.txt"
		sys_error_log.log( self )
		open(file, 'a').close()

## Save user city					
def setCity ( self, city ):

	nick = self.get_nick()
	city = city.title().strip() 
	file = "modules/data/fmi_nicks.txt"
	
	## If the nick is in the file, loop through it and replace the line containing the nick
	## with the new city. We write the whole new file to temp.txt and then move it back to fmi_nicks.txt
	try:
		#f = open(file)
		if re.search("\\b"+nick+":\\b", open(file).read(), flags=re.IGNORECASE):
			with open("modules/data/temp.txt", "w", encoding="UTF-8") as temp:
				for line in open(file):				
					str = "{0}:{1}".format(nick,city)
					temp.write(re.sub("^{0}:.*$".format(nick), str, line))
				os.remove("modules/data/fmi_nicks.txt")
				os.rename("modules/data/temp.txt", file)
			return(True)
		## If the nick doesn't exist in the file, append it in there
		else:
			with open(file, "a", encoding="UTF-8") as file:
				str = "\r\n{0}:{1}".format(nick,city)
				file.write(str)
			return(True)
	except Exception as e:
		self.errormsg = "[ERROR]-[fmi] setCity() stating: {0}".format(e)
		sys_error_log.log( self ) ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
