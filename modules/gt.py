import urllib.parse
import syscmd
from bs4 import BeautifulSoup

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
			if self.config["debug"] == "true":
				print("Someting went wrong getting the html")
		try:
			try:
				soup = BeautifulSoup(html, "lxml")
			except:
				soup = BeautifulSoup(html, "html5lib")
			## Get the translation
			data = soup.findAll("div", {"class" : "t0"})
			self.send_chan(data[0].string.strip())
		except Exception as e:
			if self.config["debug"] == "true":
				print("[ERROR]-[gt] gt() stating: {0}".format(e))
