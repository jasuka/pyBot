import urllib.parse
import syscmd
from bs4 import BeautifulSoup
import sysErrorLog

def gt(self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !gt <from> <to> <word/sentence>")
	else:
		try:
			parameters = ""
			frm = self.msg[4].strip()
			to = self.msg[5].strip()
			length = len(self.msg)
			
			for x in range (6, length):
				parameters += "{0} ".format(self.msg[x])
			parameters_url = urllib.parse.quote(parameters.strip())
			url = "http://translate.google.com/m?hl={0}&sl={1}&ie=UTF-8&q={2}".format(to, frm, parameters_url)
			html = syscmd.getHtml(self, url, True )
		except:
			self.errormsg = "[NOTICE]-[gt] Something went wrong getting the html"
			sysErrorLog.log( self )
			
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html.parser")
			#else:
			#	soup = BeautifulSoup(html, "html5lib") Umlauts Broken!
			## Get the translation
			data = soup.findAll("div", {"class" : "t0"})
			if data:
				self.send_chan(data[0].string.strip())
			else:
				return
		except Exception as e:
			self.errormsg = "[ERROR]-[gt] gt() stating: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
