import urllib.request
from bs4 import BeautifulSoup
import re

def title ( self, url ):
	
	valid = re.search( ".*\.(jpg$|jpeg$|png$|gif$|pdf$|exe$|zip$)", url )

	if valid == None:
		print("Ei tulla tänne")
		user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
		headers = { 'User-Agent' : user_agent }
		req = urllib.request.Request(url, None, headers)
		try:
			html = urllib.request.urlopen(req).read()
		except urllib.error.HTTPError as msg:
			self.send_chan( str(msg) )
		try:
			soup = BeautifulSoup(html)
			title = soup.title.string
			self.send_chan( "~ " + title )
		except:
			pass
		