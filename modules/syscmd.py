import urllib.request
import os
import re
import time
import sys_error_log
import socket

## Get HTML for given url
def getHtml( self, url, useragent):
	try:
		if useragent == True:
			user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
			headers = { 'User-Agent' : user_agent }
			req = urllib.request.Request(url, None, headers)
		else:
			req = urllib.request.Request(url, None)
			
		html = urllib.request.urlopen(req, timeout = 20).read()
		return(html)
	except Exception as e:
		self.errormsg = "[ERROR]-[syscmd] getHtml() stating: {0}".format(e)
		sys_error_log.log ( self ) ## LOG the error
		self.send_chan( "~ {0}".format(e))
## End

## Check if the city exists in Finland
def checkCity ( city ):

	try:
		city = city.title().strip()
		with open("modules/data/cities.txt", "r", encoding="UTF-8") as file:
			data = [x.strip() for x in file.readlines()]

		if city in data:
			return(True)
	except IOError as e:
		self.errormsg = "[ERROR]-[syscmd] checkCity() stating: {0}".format(e)
		sys_error_log.log( self ) ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
## End

## Clears html tags from a string
def delHtml( html ):
	try:
		html = re.sub('<[^<]+?>', '', html)
		return(html)
	except Exception as e:
		self.errormsg = "[ERROR]-[syscmd] delHtml() stating: {0}".format(e)
		sys_error_log.log( self ) ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
			
## End

## Automodes checkup on event JOIN
def modecheck (self):
	file = "modules/data/automodes.txt"
	line2 = ""
	try:
		with open(file, "r", encoding="UTF-8") as modes:
			for line in modes:
				spl = line.split(";")
				#print(spl[0])
				line2 += spl[0]+","
			#line2 = line2.join(",")
			#print(line2)
			if self.get_host() in line2:
				if spl[1].strip() == "ao":
					self.send_data("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
					print("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
				elif spl[1].strip() == "av":
					self.send_data("MODE {0} +v {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
					print("MODE {0} +v {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
			#line2 = ""
	except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
		open(file, "a").close()
		self.errormsg = "[NOTICE]-[syscmd] modcheck(): Creating file for automodes '{0}'".format(file)
		sys_error_log.log ( self )
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))

## End

## ADD AUTOMODE
def addautomode (self,modes,chan):
	
	identhost = self.hostident.strip() 	#this is created by getRemoteHost() down below which is later on called
					   	#in core as a bot wide variable when server sends whoise code 311
	file = "modules/data/automodes.txt"

	if modes == "ao" or modes == "av":
		try:
			if re.search("\\b"+identhost+";\\b", open(file).read(), flags=re.IGNORECASE):
				with open("modules/data/temp1.txt", "w", encoding="UTF-8") as temp:
					for line in open(file):				
						str = "{0};{1};{2}".format(identhost,modes,chan)
						temp.write(re.sub("^{0};.*$".format(identhost), str, line))
					os.remove("modules/data/automodes.txt")
					os.rename("modules/data/temp1.txt", file)
				self.send_data("PRIVMSG {2} :Automode changed for {1} on channel {2}. The new mode is ({0})".format(modes,identhost,chan))
				return(True)
			## If the nick doesn't exist in the file, append it in there
			else:
				with open(file, "a", encoding="UTF-8") as file:
					str = "\r\n{0};{1};{2}".format(identhost,modes,chan)
					file.write(str)
				self.send_data("PRIVMSG {2} :Automode ({0}) added for {1} on channel {2}".format(modes,identhost,chan))
				return(True)

		except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
			open(file, "a").close()
			self.errormsg = "[NOTICE]-[syscmd] addautomode(): Creating file for automodes '{0}'".format(file)
			sys_error_log.log( self )
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
		except Exception as e:
			self.errormsg = "[ERROR]-[syscmd] addautomode() stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	else:
		self.send_data("PRIVMSG {0} :Currently the only user flags are 'ao' & 'av'".format(chan))
## END

## Return remote host based on given nick

def getRemoteHost (self):
	#print("{0}@{1}".format(self.msg[4],self.msg[5]))
	hostident = "{0}@{1}".format(self.msg[4],self.msg[5])
	return(hostident)
## End

## Replace umlauts 
def replaceUmlauts(text):
	dic = {'Ä':'%C3%84', 'ä':'%C3%A4', 'Ö':'%C3%96', 'ö':'%C3%B6', '"':'%22', '®':'%C2%AE'}
	for i, j in dic.items():
		text = text.replace(i, j)
	return text

def ipv6Connectivity():
	have_ipv6 = True
	s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	try:
		s.connect(('2a00:1450:400f:802::1000', 0))
	except:
		have_ipv6 = False
	return have_ipv6
