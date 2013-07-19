import urllib.parse
import syscmd
from bs4 import BeautifulSoup

def wiki(self):

	if len(self.msg) >= 6:
		lang = self.msg[4].strip()
		if len(lang) == 2:
			parameters = ""
			length = len(self.msg)
		
			for x in range (5, length):
				parameters += "{0} ".format(self.msg[x])
				
			parameters_url = urllib.parse.quote(parameters)
			url = "http://{0}.m.wikipedia.org/w/index.php?search={1}&fulltext=Search".format(lang,parameters_url)
			try:
				html = syscmd.getHtml(self, url, True )
			except Exception as e:
				if self.config["debug"] == "true":
					print(e)
			try:
				soup = BeautifulSoup(html)
				if len(soup.findAll("p", {"class" : "mw-search-nonefound"})) == 0:
					data = soup.findAll("div", {"class" : "mw-search-result-heading"})
					output = "{0} : http://{1}.wikipedia.org{2}".format(data[0].a.get('title'), lang, data[0].a.get('href'))
					output += " | {0} : http://{1}.wikipedia.org{2}".format(data[1].a.get('title'), lang, data[1].a.get('href'))
					self.send_chan(output)
				else:
					self.send_chan("There were no results matching the query.")
			except:
				if self.config["debug"] == "true":
						print("Parsing the html failed for some reason")
		else:
			self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland")
	else:
		self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland")