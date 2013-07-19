import urllib.parse
from bs4 import BeautifulSoup
import re
import syscmd

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
		try:
			currencies = []
			frm_ok = False
			to_ok = False
			with open("modules/data/currencies.txt", "r", encoding="UTF-8") as f:
				for line in f:
					currencies.append(line.strip())
			if frm.strip() in currencies:
				frm_ok = True
			if to.strip() in currencies:
				to_ok = True
		except FileNotFoundError:
			if self.config["debug"] == "true":
				print("modules/data/currencies.txt doesn't exist, something wrong with your bot installation!")
		## If first value is float and currencies are valid
		if isinstance( amount, float ) and frm_ok == True and to_ok == True:
			print("Moi")
			frm = urllib.parse.quote(frm)
			to = urllib.parse.quote(to)
			url = "https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(amount, frm, to)
			html = syscmd.getHtml(self, url, True)
		else:
			self.send_chan("Usage: !currency <amount> <from> <to>")	
		try:
			soup = BeautifulSoup(html)
			result = soup.findAll("div", {"id" : "currency_converter_result"})
			result = "{0}".format(result[0])
			trimmed = re.sub('<[^<]+?>', '', result)
			self.send_chan(trimmed)		
		except:
			if self.config["debug"] == "true":
				print("Parsing the html failed for some reason")
		