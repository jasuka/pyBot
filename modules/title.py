import urllib.request
from bs4 import BeautifulSoup
import re
import syscmd
import sysErrorLog

## Gets title for the urls
def title ( self, url ):
	url = syscmd.replaceUmlauts(url)
	## Banned extensions in the urls
	banned = re.search( ".*\.(jpg$|jpeg$|png$|gif$|pdf$|exe$|zip$|tar$|tar.gz$|tar.bz2$|txt$|xml$)", url )
	
	if not banned:
		url = url.strip().rstrip(".")
		## Until I figure out something better...
		if "t.co" in url.strip():
			html = syscmd.getHtml( self, url, False )
		else:
			html = syscmd.getHtml( self, url, True )
		if html:
			try:
				try:
					soup = BeautifulSoup(html, "lxml")
				except:
					soup = BeautifulSoup(html, "html.parser")
				#else:
				#	soup = BeautifulSoup(html, "html5lib") #broken!!
				## We only want to parse the title if it has been found
				if soup.title:
					title = soup.title.string
					title = re.sub("\n", "", title)
					self.send_chan( "~ " + ' '.join(title.split()) ) ##Split words and join them with space
				else:
					self.send_chan( "~ Untitled" )
			except Exception as e:
				self.errormsg = "[ERROR]-[title] title() stating: {0} ({1})".format(e, url)
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"]:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			return
