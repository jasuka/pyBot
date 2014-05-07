import urllib.request
from bs4 import BeautifulSoup
import re
import syscmd
import sysErrorLog

## Gets title for the urls
def title ( self, url ):

	if "localhost" in url:
		self.send_chan("Hah, nice try :)")
		return

	if checkContentType(self, url):	
		url = syscmd.replaceUmlauts(url)
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

def checkContentType(self, url):

	## We check the content-type from headers, if it's not text/html
	## we won't get the html (avoids downloading big files)
	try:
		req = urllib.request.Request(url, None)
		req.get_method = lambda : 'HEAD'
		response = urllib.request.urlopen(req)
		if "text/html" not in response.headers['content-type']:
			return False
		else:
			return True
	except urllib.error.URLError as e:
		if e.reason == "Method Not Allowed":
			req.get_method = lambda : 'GET'
			response = urllib.request.urlopen(req)
			if "text/html" not in response.headers['content-type']:
				return False
			else:
				return True
		else:
			self.errormsg = "[ERROR]-[syscmd] title() stating: {0}".format(e)
			sysErrorLog.log ( self ) ## LOG the error
			self.send_chan( "~ {0}".format(e))
