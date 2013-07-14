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
		user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
		headers = { 'User-Agent' : user_agent }
		req = urllib.request.Request('http://ilmatieteenlaitos.fi/saa/' + city, None, headers)
		html = urllib.request.urlopen(req).read()
	except urllib.error.HTTPError as msg:
		print(msg)
		
	try:
		soup = BeautifulSoup(html)
		str = "";
		for a,b in zip(soup.find_all("span", class_="parameter-name"), soup.find_all("span", class_="parameter-value")):
			str += " " + a.string + " " + b.string + " -"
		
			
		self.send_chan( "Sää: " + str )
	except:
		pass