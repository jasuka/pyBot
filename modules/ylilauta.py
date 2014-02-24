import urllib.parse
import syscmd
import random
from bs4 import BeautifulSoup
import sysErrorLog

def ylilauta(self):

	if len(self.msg) >= 4:
		url = "http://ylilauta.org/satunnainen/"
		try:
			html = syscmd.getHtml(self, url, True )
		except Exception as e:
			self.errormsg = "[ERROR]-[ylilauta] ylilauta()(1) stating: {0}".format(e) 
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			data = soup.findAll("span", {"class" : "postsubject"})
			x = random.randrange(0,len(data))
			string = "{0}: http:{1}".format(data[x].a.string, data[x].a.get('href'))
			self.send_chan(' '.join(string.split()))
		except Exception as e:
			self.errormsg = "[ERROR]-[ylilauta] ylilauta()(2) stating: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
