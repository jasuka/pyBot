import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sys_error_log

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
			if self.config["debug"] == "true":
				print("Someting went wrong getting the html")
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
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print(self.errormsg)
