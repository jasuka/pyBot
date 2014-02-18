import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Cache class for caching the results
class Cache:
	dataCache = []
	dataIndex = 0
	lang = ""

def wiki(self):
	if len(self.msg) < 5:
		self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland || !wiki next for the next result")
	elif len(self.msg) == 5 and self.msg[4].strip() == "next":
		if wnext(self):
			return
		else:
			self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland || !wiki next for the next result")
	elif len(self.msg) >= 6:
		Cache.lang = self.msg[4].strip()
		if syscmd.checkLang( Cache.lang ):
			wikiSearch(self)
		else:
			self.send_chan("Invalid Cache.language code!")
	else:
		self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland || !wiki next for the next result")

## Perform the wikipedia search
def wikiSearch(self):
	Cache.dataCache = []
	Cache.dataIndex = 0
	parameters = ""
	length = len(self.msg)

	for x in range (5, length):
		parameters += "{0} ".format(self.msg[x])
	parameters_url = urllib.parse.quote(parameters.strip())
	url = "http://{0}.m.wikipedia.org/w/index.php?search={1}&fulltext=Search".format(Cache.lang,parameters_url)
	try:
		html = syscmd.getHtml(self, url, True )
	except Exception as e:
		self.errormsg = "[ERROR]-[wiki] wikiSearch()(1) stating: {0}".format(e)
		sys.error_log.log( self )
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	try:
		soup = BeautifulSoup(html)
		if len(soup.findAll("p", {"class" : "mw-search-nonefound"})) == 0:
			Cache.dataCache = soup.findAll("div", {"class" : "mw-search-result-heading"})
			output = "{0}: http://{1}.wikipedia.org{2}".format(
					Cache.dataCache[Cache.dataIndex].a.get('title'), Cache.lang, Cache.dataCache[Cache.dataIndex].a.get('href'))
			self.send_chan(output)
			Cache.dataIndex += 1
		else:
			self.send_chan("There were no results matching the query.")
	except Exception as e:
		self.errormsg = "[ERROR]-[wiki] wikiSearch()(2) stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Get the next result from the cache
def wnext(self):
	if len(self.msg) == 5 and Cache.dataCache and Cache.dataIndex <= len(Cache.dataCache):
		string = "{0}: http://{1}.wikipedia.org{2}".format(
				Cache.dataCache[Cache.dataIndex].a.get('title'), Cache.lang, Cache.dataCache[Cache.dataIndex].a.get('href'))
		self.send_chan(string)
		Cache.dataIndex += 1
		return(True)
