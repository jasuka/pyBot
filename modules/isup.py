import urllib
import sys_error_log

def isup (self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !isup http://www.domain.com")
	else:
		try:
			url = self.msg[4].strip()
			if "http://" not in url:
				url = "http://" + url
			if urllib.request.urlopen("{}".format(url), None, 5).getcode() == 200:
				self.send_chan("The site {0} seems to be up!".format(url))
			else:
				self.send_chan("The site {0} seems to be down!".format(url))							
		except Exception as e:
			self.send_chan("The site {0} seems to be down!".format(url))
			self.errormsg = "[ERROR]-[isup] isup() stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
