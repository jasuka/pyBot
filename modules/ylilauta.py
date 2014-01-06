import urllib.parse
import syscmd
import random
from bs4 import BeautifulSoup
import sys_error_log

def ylilauta(self):

	if len(self.msg) >= 4:
		url = "http://ylilauta.org/satunnainen/"
		try:
			html = syscmd.getHtml(self, url, True )
		except Exception as e:
			self.errormsg = "[ERROR]-[ylilauta] ylilauta()(1) stating: {0}".format(e) 
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print(self.errormsg)
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			data = soup.findAll("span", {"class" : "postsubject"})
			x = random.randrange(0,len(data))
			string = "{0}: {1}".format(data[x].a.string, data[x].a.get('href'))
			self.send_chan(string)
		except Exception as e:
			self.errormsg = "[ERROR]-[ylilauta] ylilauta()(2) stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
					print(self.errormsg)
