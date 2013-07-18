import urllib.parse
import syscmd
from bs4 import BeautifulSoup

def youtube(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !youtube <search term>")
	else:
		#try:
			parameters = ""
			length = len(self.msg)
			for x in range (4, length):
				parameters += "{0} ".format(self.msg[x])
			parameters_url = urllib.parse.quote(parameters)
			print("Parameters: {0}".format(parameters_url))
			url = "http://youtube.com/results?search_query=" + parameters_url
			print("URL: {0}".format(url))
			html = syscmd.getHtml(self, url, True )
			print("HÖTÖMÖLÖ funkkarilta: {0}\r\n".format(html))
		#except:
			#print("Someting went wrong getting the html")
		#try:
			urls = ""
			soup = BeautifulSoup(html)
			#print("HÖTÖMÖLÖ: {0}".format(soup))
			for x in soup.findAll("a", {"class" : "yt-uix-tile-link"})[0:2]:
				print(x.get('title'))
				print(x.get('href'))
			for x in soup.findAll("a", {"class" : "yt-uix-tile-link"})[0:2]:
				urls += "{0}: http://youtube.com{1} | ".format(x.get('title'), x.get('href'))
			if len(urls) > 0:
				self.send_chan(urls.strip()[:-1])
			else:
				self.send_chan("No results for: {0}".format(parameters))
		#except:
		#	pass