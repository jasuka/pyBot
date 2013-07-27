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
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			else:
				soup = BeautifulSoup(html, "html.parser")
			title = soup.title.string
			title = re.sub("\n", "", title).strip()
			self.send_chan( "~ " + title )
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)