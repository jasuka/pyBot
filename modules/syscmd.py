import urllib.request

## Get HTML for given url
def getHtml( self, url, useragent):
	try:
		if useragent == True:
			user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
			headers = { 'User-Agent' : user_agent }
			req = urllib.request.Request(url, None, headers)
		else:
			req = urllib.request.Request(url, None)
			
		html = urllib.request.urlopen(req).read()
		return(html)
	except urllib.error.HTTPError as msg:
		return(msg)
	except:
		if self.config["debug"] == "true":
			print("Fetching data faile for some reason")
## End

 