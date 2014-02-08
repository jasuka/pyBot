import urllib.parse
from bs4 import BeautifulSoup
import re
import syscmd
import sysErrorLog

def currency( self ):

	if len(self.msg) < 7:
		self.send_chan("Usage: !currency <amount> <from> <to>")
	if len(self.msg) == 7:
		try:
			amount = float(self.msg[4])
		except ValueError:
			amount = 1.00
		frm = self.msg[5].upper()
		to = self.msg[6].upper()

		## If first value is float and currencies are valid
		if isinstance( amount, float ) and syscmd.checkCurrency( frm, to):
			frm = urllib.parse.quote(frm)
			to = urllib.parse.quote(to)
			url = "https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(amount, frm, to)
			html = syscmd.getHtml(self, url, True)
			try:
				soup = BeautifulSoup(html)
				result = soup.findAll("div", {"id" : "currency_converter_result"})
				result = "{0}".format(result[0])
				trimmed = re.sub('<[^<]+?>', '', result)
				self.send_chan(trimmed)		
			except Exception as e:
				self.errormsg = "[ERROR]-[Currency] stating: {0}".format(e)
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"] == "true":
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			self.send_chan("Usage: !currency <amount> <from> <to>")	

		
