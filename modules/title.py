import urllib.request
from bs4 import BeautifulSoup
import re
import syscmd
import sys_error_log

## Gets title for the urls
def title ( self, url ):
	url = syscmd.replaceUmlauts(url)
	## Banned extensions in the urls
	banned = re.search( ".*\.(jpg$|jpeg$|png$|gif$|pdf$|exe$|zip$|txt$)", url )
	
	if not banned:
		url = url.strip().rstrip(".")
		#req = urllib.request.Request(url, None)
		## Until I figure out something better...
		if "t.co" in url.strip():
			html = syscmd.getHtml( self, url, False )
		else:
			html = syscmd.getHtml( self, url, True )
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html.parser")
			#else:
			#	soup = BeautifulSoup(html, "html5lib") #broken!!
			title = soup.title.string
			title = re.sub("\n", "", title)
			self.send_chan( "~ " + ' '.join(title.split()) ) ##Split words and join them with space
		except Exception as e:
			self.errormsg = "[ERROR]-[title] title() stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print(self.errormsg)
