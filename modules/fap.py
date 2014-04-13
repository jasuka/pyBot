import urllib.parse
import syscmd
import random
from bs4 import BeautifulSoup
import sysErrorLog

def fap(self):

	if len(self.msg) >= 4:
		if len(self.msg) == 4:
			page = random.randrange(1,6000)
			url = "http://www.porn.com/videos.html?p={0}".format(page)
		elif len(self.msg) > 4:
			parameters = ""
			for x in range (4, len(self.msg)):
				parameters += "{0} ".format(self.msg[x])
			parameters_url = urllib.parse.quote(parameters.strip())
			url = "http://www.porn.com/search.html?q={0}".format(parameters_url)
		try:
			html = syscmd.getHtml(self, url, True )
		except Exception as e:
			self.errormsg = "[ERROR]-[fap] fap()(1) stating: {0}".format(e) 
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		if html:
			try:
				try:
					soup = BeautifulSoup(html, "lxml")
				except:
					soup = BeautifulSoup(html, "html.parser")
				data = soup.findAll("a", {"class" : "title"})
				if len(data) > 0:
					x = random.randrange(0,len(data))
					string = "{0}: http://www.porn.com{1}".format(data[x].get('title'), data[x].get('href'))
					self.send_chan(' '.join(string.split()))
				else:
					self.send_chan("No results for: {0}".format(parameters))
			except Exception as e:
				print(e)
				self.errormsg = "[ERROR]-[fap] fap()(2) stating: {0}".format(e)
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"]:
						print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			self.send_chan("No results for: {0}".format(parameters))