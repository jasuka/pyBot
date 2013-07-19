#ul class mw-search-results -> li -> div -> a  = title and link
#div searchresult -> span class searchmatch = text

import urllib.parse
import syscmd
from bs4 import BeautifulSoup

def wiki(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !wiki <search term>")
	else:
		try:
			parameters = ""
			length = len(self.msg)
			
			for x in range (4, length):
				parameters += "{0} ".format(self.msg[x])
			parameters_url = urllib.parse.quote(parameters)
			
			url = "http://en.m.wikipedia.org/w/index.php?search=" + parameters_url + "&fulltext=Search"
			html = syscmd.getHtml(self, url, True )
		except:
			if self.config["debug"] == "true":
				print("Someting went wrong getting the html")
		try:
			soup = BeautifulSoup(html)
			if len(soup.findAll("p", {"class" : "mw-search-nonefound"})) == 0:
				data = soup.findAll("div", {"class" : "mw-search-result-heading"})
				output = "{0} : http://en.wikipedia.org{1}".format(data[0].a.get('title'), data[0].a.get('href'))
				output += " | {0} : http://en.wikipedia.org{1}".format(data[1].a.get('title'), data[1].a.get('href'))
				#print(data[0].
				self.send_chan(output)
			else:
				self.send_chan("There were no results matching the query.")
		except:
			if self.config["debug"] == "true":
				print("Parsing the html failed for some reason")