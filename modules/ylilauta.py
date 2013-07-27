import urllib.parse
import syscmd
import random
from bs4 import BeautifulSoup

def ylilauta(self):

	if len(self.msg) >= 4:
		url = "http://ylilauta.org/satunnainen/"
		try:
			html = syscmd.getHtml(self, url, True )
		except Exception as e:
			if self.config["debug"] == "true":
				print(e)
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			data = soup.findAll("span", {"class" : "postsubject"})
			x = random.randrange(0,len(data))
			string = "{0}: {1}".format(data[x].a.string, data[x].a.get('href'))
			self.send_chan(string)
		except Exception as e:
			if self.config["debug"] == "true":
					print(e)