import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Global variables for caching the search result
## and for the next functionality
dataCache = []
dataIndex = 0

def google(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !google <search term>")
	if len(self.msg) == 5 and self.msg[4].strip() == "next":
		if gnext(self):
			return
		else:
			googleSearch(self)
	else:
		googleSearch(self)

## Performs the google search
def googleSearch(self):
	try:
		## Global variables for caching the result
		## and for the next functionality
		global dataCache
		global dataIndex
		dataCache = []
		dataIndex = 0
		parameters = ""
		length = len(self.msg)
		
		for x in range (4, length):
			parameters += "{0} ".format(self.msg[x])
		parameters_url = urllib.parse.quote(parameters)
		
		url = "https://www.google.fi/search?q=" + parameters_url
		html = syscmd.getHtml(self, url, True )
	except:
		self.errormsg = "[NOTICE]-[google] Something went wrong getting the html"
		sysErrorLog.log( self )
		
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
	try:
		try:
			soup = BeautifulSoup(html, "lxml")
		except:
			soup = BeautifulSoup(html, "html5lib")
		## Get the first
		dataCache = soup.findAll("h3", {"class" : "r"})
		if len(dataCache) > 0:
			title = "{0}".format(dataCache[dataIndex].a)
			title = syscmd.delHtml(title)
			string = "{0}: {1}".format(title, dataCache[dataIndex].a.get('href'))
			self.send_chan(string)
			dataIndex += 1
		else:
			self.send_chan("No results for: {0}".format(parameters))
	except Exception as e:
		self.errormsg = "[ERROR]-[google] google() stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Gets the next result from the cache
def gnext(self):
	## Global variables for getting
	## the data from cache when issuing
	## !google next
	global dataCache
	global dataIndex
	if len(self.msg) == 5 and dataCache and dataIndex <= len(dataCache):
		title = "{0}".format(dataCache[dataIndex].a)
		title = syscmd.delHtml(title)
		string = "{0}: {1}".format(title, dataCache[dataIndex].a.get('href'))
		if len(dataCache) > 0:
			self.send_chan(string)
			dataIndex += 1
			return(True)
	else:
		return(False)


