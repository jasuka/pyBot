import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Cache class for caching the results
class Cache:
	dataCache = []
	dataIndex = 0

def stack(self):
	if len(self.msg) == 4:
		self.send_chan("Usage: !stack <search term> || Usage: !stack next for the next result")
		return
	if len(self.msg) == 5 and self.msg[4].strip() == "next":
		if snext(self):
			return
		else:
			stackSearch(self)
	else:
		stackSearch(self)

## Performs the stackoverflow search
def stackSearch(self):
	try:
		Cache.dataCache = []
		Cache.dataIndex = 0
		parameters = ""
		length = len(self.msg)
		
		for x in range (4, length):
			parameters += "{0} ".format(self.msg[x])
		parameters_url = urllib.parse.quote(parameters.strip())
		url = "http://stackoverflow.com/search?q=" + parameters_url
		html = syscmd.getHtml(self, url, True )
	except:
		self.errormsg = "[NOTICE]-[stackoverflow] stackSearch()(1) Something went wrong getting the html"
		sysErrorLog.log( self )
		
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
	try:
		try:
			soup = BeautifulSoup(html, "lxml")
		except:
			soup = BeautifulSoup(html, "html5lib")
		Cache.dataCache = soup.findAll("div", {"class" : "result-link"})
		if len(Cache.dataCache) > 0:
			title = "{0}".format(Cache.dataCache[Cache.dataIndex].a)
			title = syscmd.delHtml(title)
			string = "{0}: http://stackoverflow.com{1}".format(title.strip(), Cache.dataCache[Cache.dataIndex].a.get('href').strip())
			self.send_chan(string)
			Cache.dataIndex += 1
		else:
			self.send_chan("No results for: {0}".format(parameters))
	except Exception as e:
		self.errormsg = "[ERROR]-[stackoverflow] stackSearch()(2) stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Gets the next result from the cache
def snext(self):
	if len(self.msg) == 5 and Cache.dataCache and Cache.dataIndex <= len(Cache.dataCache):
		title = "{0}".format(Cache.dataCache[Cache.dataIndex].a)
		title = syscmd.delHtml(title)
		string = "{0}: http://stackoverflow.com{1}".format(title.strip(), Cache.dataCache[Cache.dataIndex].a.get('href').strip())
		self.send_chan(string)
		Cache.dataIndex += 1
		return(True)
