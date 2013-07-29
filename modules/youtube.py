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
			
			url = "http://m.youtube.com/results?search_query=" + parameters_url
			html = syscmd.getHtml(self, url, True )
		except:
			if self.config["debug"] == "true":
				print("Someting went wrong getting the html")
		try:
			urls = ""
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			#else:
			#	soup = BeautifulSoup(html, "html.parser")
			## Get the first two urls, note to self: optimize the code if you can think how ;)
			for x in soup.findAll("a", {"class" : "yt-uix-tile-link"})[0:1]:
				href = x.get('href')
				href = href[-11:]
				urls += "{1}: http://youtube.com/watch?v={0} | ".format(href, x.get('title'))
			if len(urls) > 0:
				self.send_chan(urls.strip()[:-1])
			else:
				self.send_chan("No results for: {0}".format(parameters))
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)