import urllib.request
from bs4 import BeautifulSoup
import re

def currency( self ):
	
	amount = 0
	frm = "eur"
	to = "usd"
	try:
		if len(self.msg) < 7:
			self.send_chan("Usage: !currency <amount> <from> <to>")
		else:
			
			try:
				amount = float(self.msg[4])
			except ValueError:
				pass
			frm = self.msg[5]
			to = self.msg[6]
		if isinstance( amount, float ):
			frm = urllib.parse.quote(frm)
			to = urllib.parse.quote(to)
			user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
			headers = { 'User-Agent' : user_agent }
			req = urllib.request.Request("https://www.google.com/finance/converter?a={0}&from={1}&to={2}".format(
										amount, frm, to), None, headers)
										
			html = urllib.request.urlopen(req).read()
		else:
			self.send_chan("Usage: !currency <amount> <from> <to>")
			
	except urllib.error.HTTPError as msg:
		print(msg)
		
	try:
		soup = BeautifulSoup(html)
		result = soup.findAll("div", {"id" : "currency_converter_result"})
		result = "{0}".format(result[0])
		trimmed = re.sub('<[^<]+?>', '', result)
		self.send_chan(trimmed)
		
	except:
		pass
		