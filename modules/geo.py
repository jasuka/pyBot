import urllib.request
import json

def geo (self):

	if len(self.msg) == 4:
		self.send_chan("Usage: !geo <ip/host>")
	else:
		try:
			data = json.loads(urllib.request.urlopen("http://ip-api.com/json/{0}".format(
								self.msg[4])).read().decode("utf-8"))
			shortened = urllib.request.urlopen("http://is.gd/create.php?format=simple&url={0}".format(
								urllib.parse.quote("https://www.google.com/maps?q={0},{1}&output=classic".format(
								data["lat"],data["lon"])))).read().decode("utf-8")
								
			self.send_chan(("IP: {0}  ISP: {1}  COUNTRY: {2}  MAP: {3}".format(
							data["query"], data["isp"], data["country"], shortened)))
		except Exception as e:
			if self.config["debug"] == "true":
				print("Error occured in geo module: " +e)
