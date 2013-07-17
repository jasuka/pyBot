#a class="yt-uix-sessionlink yt-uix-tile-link yt-uix-contextlink "
import urllib.parse
import syscmd
from bs4 import BeautifulSoup

def youtube(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !youtube <search term>")
	else:
		try:
			parameters = ""
			length = len(self.msg)
			for x in range (4, length):
				parameters += "{0} ".format(self.msg[x])
			parameters_url = urllib.parse.quote(parameters)
			url = "http://www.youtube.com/results?search_query=" + parameters_url
			print(url)
			html = syscmd.getHtml(self, url, True )
		except:
			print("Kusahti")
		try:
			urls = ""
			soup = BeautifulSoup(html)
			for x in soup.findAll("a", {"class" : "yt-uix-tile-link"})[0:3]:
				urls += "{0}: http://www.youtube.com{1} | ".format(x.get('title'), x.get('href'))
			if len(urls) > 0:
				self.send_chan(urls.strip()[:-1])
			else:
				self.send_chan("No results for: {0}".format(parameters))
		except:
			pass