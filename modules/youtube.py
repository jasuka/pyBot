import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Cache class for caching the results
class Cache:
	dataCache = []
	dataIndex = 0

def youtube(self):
	if len(self.msg) == 4:
		self.send_chan("Usage: !youtube <search term> || !youtube next for the next result")
	elif len(self.msg) == 5 and self.msg[4].strip() == "next":
		if ynext(self):
			return
		else:
			youtubeSearch(self)
	else:
		youtubeSearch(self) 

## Performs the youtube search
def youtubeSearch(self):
	try:
		Cache.dataCache = []
		Cache.dataIndex = 0

		parameters = ""
		length = len(self.msg)

		for x in range (4, length):
			parameters += "{0} ".format(self.msg[x])
		parameters_url = urllib.parse.quote(parameters.strip())
		
		url = "http://m.youtube.com/results?search_query={0}".format(parameters_url)
		html = syscmd.getHtml(self, url, True )
	except: 
		self.errormsg = "[ERROR]-[youtube] youtubeSearch()(1) Someting went wrong getting the html"
		sysErrorLog.log( self ) ## Log the error
		
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	try:
		urls = ""
		try:
			soup = BeautifulSoup(html, "lxml")
		except:
			soup = BeautifulSoup(html, "html5lib")
		Cache.dataCache = soup.findAll("a", {"class" : "yt-uix-tile-link"})
		if len(Cache.dataCache) > 0:
			string = "{1}: http://youtube.com/watch?v={0} | ".format(
					Cache.dataCache[Cache.dataIndex].get('href')[-11:], Cache.dataCache[Cache.dataIndex].get('title'))
			self.send_chan(string)
			Cache.dataIndex += 1
		else:
			self.send_chan("No results for: {0}".format(parameters))
	except Exception as e:
		self.errormsg = "[ERROR]-[youtube] youtubeSearch()(2) stating: {0}".format(e)
		sysErrorLog.log ( self ) ## Log the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Get the next result from the cache
def ynext(self):
	if len(self.msg) == 5 and Cache.dataCache and Cache.dataIndex <= len(Cache.dataCache):
		string = "{1}: http://youtube.com/watch?v={0} | ".format(
				Cache.dataCache[Cache.dataIndex].get('href')[-11:], Cache.dataCache[Cache.dataIndex].get('title'))
		self.send_chan(string)
		Cache.dataIndex += 1
		return(True)

