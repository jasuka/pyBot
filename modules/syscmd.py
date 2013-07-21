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
			
		html = urllib.request.urlopen(req, timeout = 10).read()
		return(html)
	except HTTPError:
		self.send_chan( "{0}".format(e) )
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)
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