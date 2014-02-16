import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Global variables for caching the search result
## and for the next functionality
dataCache = []
dataIndex = 0

def youtube(self):
	if len(self.msg) == 4:
		self.send_chan("Usage: !youtube <search term>")
	if len(self.msg) == 5 and self.msg[4].strip() == "next":
		if ynext(self):
			return
		else:
			youtubeSearch(self)
	else:
		youtubeSearch(self)

## Performs the youtube search
def youtubeSearch(self):
	try:
		global dataCache
		global dataIndex
		dataCache = []
		dataIndex = 0
		parameters = ""
		length = len(self.msg)
		
		for x in range (4, length):
			parameters += "{0} ".format(self.msg[x])
		parameters_url = urllib.parse.quote(parameters)
		
		url = "http://m.youtube.com/results?search_query=" + parameters_url
		html = syscmd.getHtml(self, url, True )
	except: 
		self.errormsg = "[ERROR]-[youtube] Someting went wrong getting the html"
		sysErrorLog.log( self ) ## Log the error
		
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	try:
		urls = ""
		try:
			soup = BeautifulSoup(html, "lxml")
		except:
			soup = BeautifulSoup(html, "html5lib")
		## Get all results
		dataCache = soup.findAll("a", {"class" : "yt-uix-tile-link"})
		if len(dataCache) > 0:
			string = "{1}: http://youtube.com/watch?v={0} | ".format(
					dataCache[dataIndex].get('href')[-11:], dataCache[dataIndex].get('title'))
			self.send_chan(string)
			dataIndex += 1
		else:
			self.send_chan("No results for: {0}".format(parameters))
	except Exception as e:
		self.errormsg = "[ERROR]-[youtube] youtube() stating: {0}".format(e)
		sysErrorLog.log ( self ) ## Log the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Get the next result from the cache
def ynext(self):
	## Global variables for getting
	## the data from cache when issuing
	## !google next
	global dataCache
	global dataIndex
	if len(self.msg) == 5 and dataCache and dataIndex <= len(dataCache):
		string = "{1}: http://youtube.com/watch?v={0} | ".format(
				dataCache[dataIndex].get('href')[-11:], dataCache[dataIndex].get('title'))
		self.send_chan(string)
		dataIndex += 1
		return(True)

