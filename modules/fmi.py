import urllib.request
from bs4 import BeautifulSoup
import re

def fmi( self ):

	try:
		city = self.msg[4]
	except IndexError:
		self.send_chan( "Anna kaupunki" )
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
			
		html = urllib.request.urlopen(req).read()
		
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

		for a in str:
			text += "%s - " % a
			
		trimmed = re.sub('<[^<]+?>', '', text)

		output = city.strip().title() + " klo " + time + ": " + trimmed	
		self.send_chan( output )
	except:
		pass
		