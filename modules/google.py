import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Cache class for caching the results
class Cache:
	dataCache = []
	dataIndex = 0

def google(self):
	if len(self.msg) == 4:
		self.send_chan("Usage: !google <search term> || next for the next result")
	elif len(self.msg) == 5 and self.msg[4].strip() == "next":
		if gnext(self):
			return
		else:
			googleSearch(self)
	else:
		googleSearch(self)

## Performs the google search
def googleSearch(self):
	try:
		Cache.dataCache = []
		Cache.dataIndex = 0
		parameters = ""
		length = len(self.msg)
		
		for x in range (4, length):
			parameters += "{0} ".format(self.msg[x])
		parameters_url = urllib.parse.quote(parameters.strip())
		
		url = "https://www.google.fi/search?q={0}".format(parameters_url)
		html = syscmd.getHtml(self, url, True )
	except:
		self.errormsg = "[NOTICE]-[google] googleSearch()(1) Something went wrong getting the html"
		sysErrorLog.log( self )
		
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
	try:
		try:
			soup = BeautifulSoup(html, "lxml")
		except:
			soup = BeautifulSoup(html, "html5lib")
		## Get the first
		Cache.dataCache = soup.findAll("h3", {"class" : "r"})
		if len(Cache.dataCache) > 0:
			title = "{0}".format(Cache.dataCache[Cache.dataIndex].a)
			title = syscmd.delHtml(title)
			string = "{0}: {1}".format(title, Cache.dataCache[Cache.dataIndex].a.get('href'))
			self.send_chan(string)
			Cache.dataIndex += 1
		else:
			self.send_chan("No results for: {0}".format(parameters))
	except Exception as e:
		self.errormsg = "[ERROR]-[google] googleSearch()(2) stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Gets the next result from the cache
def gnext(self):
	if len(self.msg) == 5 and Cache.dataCache and Cache.dataIndex <= len(Cache.dataCache):
		title = "{0}".format(Cache.dataCache[Cache.dataIndex].a)
		title = syscmd.delHtml(title)
		string = "{0}: {1}".format(title, Cache.dataCache[Cache.dataIndex].a.get('href'))
		self.send_chan(string)
		Cache.dataIndex += 1
		return(True)
