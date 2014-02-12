import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

def google(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !google <search term>")
	else:
		try:
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
			data = soup.findAll("h3", {"class" : "r"})
			title = "{0}".format(data[0].a)
			title = syscmd.delHtml(title)
			string = "{0}: {1}".format(title, data[0].a.get('href'))
			if len(data) > 0:
				self.send_chan(string)
			else:
				self.send_chan("No results for: {0}".format(parameters))
		except Exception as e:
			self.errormsg = "[ERROR]-[google] google() stating: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
