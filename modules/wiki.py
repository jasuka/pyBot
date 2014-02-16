import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

## Global variables for caching the search result
## and for the next functionality
dataCache = []
dataIndex = 0
lang = ""

def wiki(self):
	global lang
	if len(self.msg) < 5:
		self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland")
	elif len(self.msg) == 5 and self.msg[4].strip() == "next":
		if wnext(self, lang):
			return
		else:
			self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland")
	elif len(self.msg) >= 6:
		lang = self.msg[4].strip()
		if syscmd.checkLang( lang ):
			wikiSearch(self, lang)
		else:
			self.send_chan("Invalid language code!")
	else:
		self.send_chan("Usage: !wiki <lang> <search term> - e.g. !wiki en finland")

## Perform the wikipedia search
def wikiSearch(self, lang):

	## Global variables for caching the search result
	## and for the next functionality
	global dataCache
	global dataIndex
	dataCache = []
	dataIndex = 0
	parameters = ""
	length = len(self.msg)

	for x in range (5, length):
		parameters += "{0} ".format(self.msg[x])
		
	parameters_url = urllib.parse.quote(parameters)
	url = "http://{0}.m.wikipedia.org/w/index.php?search={1}&fulltext=Search".format(lang,parameters_url)
	try:
		html = syscmd.getHtml(self, url, True )
	except Exception as e:
		self.errormsg = "[ERROR]-[wiki] wiki()(1) stating: {0}".format(e)
		sys.error_log.log( self )
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	try:
		soup = BeautifulSoup(html)
		if len(soup.findAll("p", {"class" : "mw-search-nonefound"})) == 0:
			dataCache = soup.findAll("div", {"class" : "mw-search-result-heading"})
			output = "{0}: http://{1}.wikipedia.org{2}".format(
					dataCache[dataIndex].a.get('title'), lang, dataCache[dataIndex].a.get('href'))
			self.send_chan(output)
			dataIndex += 1
		else:
			self.send_chan("There were no results matching the query.")
	except Exception as e:
		self.errormsg = "[ERROR]-[wiki] wiki()(2) stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Get the next result from the cache
def wnext(self, lang):
	## Global variables for getting
	## the data from cache when issuing
	## !google next
	global dataCache
	global dataIndex
	if len(self.msg) == 5 and dataCache and dataIndex <= len(dataCache):
		string = "{0}: http://{1}.wikipedia.org{2}".format(
				dataCache[dataIndex].a.get('title'), lang, dataCache[dataIndex].a.get('href'))
		self.send_chan(string)
		dataIndex += 1
		return(True)
