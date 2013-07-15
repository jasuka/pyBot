import urllib.request
from bs4 import BeautifulSoup
import re
import os

def fmi( self ):
	
	try:
		city = self.msg[4]		
		city = city.title().strip()
		
	except IndexError:
		self.send_chan( "2 Usage: !fmi <city> | !fmi set <city>" )
		raise
		
	try:
		city = city.title().strip()
		user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
		headers = { 'User-Agent' : user_agent }
		req = urllib.request.Request("http://ilmatieteenlaitos.fi/saa/" + city, None, headers)
		
		if city == "Oulu":
			req = urllib.request.Request("http://ilmatieteenlaitos.fi/saa/" + city + "?&station=101799", None, headers)
		if city == "Helsinki":
			req = urllib.request.Request("http://ilmatieteenlaitos.fi/saa/" + city + "?&station=100971", None, headers)
			
		#html = urllib.request.urlopen(req).read()
		
	except urllib.error.HTTPError as msg:
		print(msg)
		
	try:
		soup = BeautifulSoup(html)
		text = ""
		## When the weather was updated
		time = soup.find_all("span", class_="time-stamp")
		time = time[0].string
		time = time[10:-12]

		str = soup.findAll("span", {"class" : "parameter-name-value"})
		
		## Loop the reusts into a string
		for a in str:
			text += "{0} - ".format(a)
		
		## Remove Html tags	
		trimmed = re.sub('<[^<]+?>', '', text)

		output = city.strip() + " klo " + time + ": " + trimmed	
		##self.send_chan( output )
	except:
		pass

## Return saved city for the nick
def sys_getcity ( self, nick ):

	nick = self.get_nick()
	file = "modules/data/fmi_nicks.txt"
	
	with open(file, "r", encoding="UTF-8") as f:
		for line in f:
			if nick in line:
				city = line.split(":")
				return(city[1])

def sys_setcity ( self, city ):

	nick = self.get_nick()
	city = city.title().strip() 
	file = "modules/data/fmi_nicks.txt"
	n = ""
	if nick in open(file).read():
		with open("modules/data/temp.txt", "w", encoding="UTF-8") as temp:
			for line in open(file):				
				str = "{0}:{1}".format(nick,city)
				temp.write(re.sub("^{0}:.*$".format(nick), str, line))
			os.remove("modules/data/fmi_nicks.txt")
			os.rename("modules/data/temp.txt", file)
		return(True)
	else:
		with open(file, "a", encoding="UTF-8") as file:
			str = "\r\n{0}:{1}".format(nick,city)
			file.write(str)
		return(True)

