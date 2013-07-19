import urllib.request
from bs4 import BeautifulSoup
import re
import syscmd

## Gets title for the urls
def title ( self, url ):
	
	## Banned extensions in the urls
	valid = re.search( ".*\.(jpg$|jpeg$|png$|gif$|pdf$|exe$|zip$)", url )
	
	if valid == None:
		req = urllib.request.Request(url, None)
		html = syscmd.getHtml( self, url, True )
		try:
			soup = BeautifulSoup(html, "lxml")
			title = soup.title.string
			title = re.sub("\n", "", title).strip()
			self.send_chan( "~ " + title )
		except:
			if self.config["debug"] == "true":
				print("Parsing the html failed for some reason")