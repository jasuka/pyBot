import urllib

def isup (self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !isup http://www.domain.com")
	else:
		try:
			url = self.msg[4].strip()
			if "http://" not in url:
				url = "http://" + url
			if urllib.request.urlopen("{}".format(url)).getcode() == 200:
				self.send_chan("The site {0} seems to be up!".format(url))
			else:
				self.send_chan("The site {0} seems to be down!".format(url))							
		except Exception as e:
			self.send_chan("The site {0} seems to be down!".format(url))
			if self.config["debug"] == "true":
				print(e)