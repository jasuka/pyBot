
## BASH colors used before the main class
pRed = "\033[0;31m"
pBlue = "\033[0;34m"
pGreen = "\033[0;32m"
pEnd = "\033[0m"

## Import needed modules
import socket
import re
import random
import sys
import time
import importlib
import imp
import os
from threading import Thread

sys.path.insert(1, './sysmodules') ## Path for the modules
sys.path.insert(2, './modules') ## Path for the modules
## Import Config
import config
## Import modules config
import modulecfg

## Loading system modules ##

print("\r\n####################")
print("#  {0}System modules{1}  #".format(pRed, pEnd))
print("####################\r\n")

try:
	for mod in modulecfg.modulecfg["sysmodules"].split(","):
		print("Loading system module {0}{1}{2}".format(pBlue, mod, pEnd))
		globals()[mod] = __import__(mod)

except (ImportError, SyntaxError) as e:
	print("{0}Couldn't load system module: {1}{2}".format(pRed, mod, pEnd))
	if config.config["debug"]:
		print("{0}{1}{2}".format(pRed, e, pEnd))
	raise

except Exception as e: ## Is this exception really needed here ???
	if config.config["debug"]:
		print("[ERROR]-[Core] Load modules: {0} , This error is not being logged".format(e))

print("\r\n##########################################")
print("# {0}All system modules loaded successfully{1} #".format(pGreen, pEnd))
print("##########################################\r\n")

## Loading user modules ##

print("##################")
print("#  {0}User modules{1}  #".format(pRed, pEnd))
print("##################\r\n")

brokenModule = [] 	# A list of broken modules
mLoaded = []		# A list of loaded modules
toLoad = len(modulecfg.modulecfg["modules"].split(",")) # How many modules to load
doneLoading = False

while not doneLoading:
	try:
		for mod in modulecfg.modulecfg["modules"].split(","):
			if mod not in brokenModule and mod not in mLoaded:
				print("Loading module {0}{1}{2}".format(pBlue, mod, pEnd))
				globals()[mod] = __import__(mod)
				mLoaded.append(mod)

	except (ImportError, SyntaxError) as e:
		toLoad -= 1
		brokenModule.append(mod)
		print("{0}Couldn't load module: {1}{2}".format(pRed, mod, pEnd))
		if config.config["debug"]:
			print("{0}{1}{2}".format(pRed, e, pEnd))

	except Exception as e: ## Is this exception really needed here ???
		if config.config["debug"]:
			print("[ERROR]-[Core] Load modules: {0} , This error is not being logged".format(e))

	finally:
		if len(mLoaded) == toLoad: 
			doneLoading = True
			print("\r\n#################################")
			print("# {0}Finished loading user modules{1} #".format(pGreen, pEnd))
			print("#################################\r\n")

## Global variable for the flood protection
flood = {}

## Class pyBot
class pyBot():
	def __init__( self ):
	
	## Bot Version
		self.version = "pyBot version 1.0"
		print("{0}[[You are running the {1}]]{2}\r\n"
			.format(self.color("blue"),self.version,self.color("end")))

	## Config and start the bot
		self.config = config.config
		self.modulecfg = modulecfg.modulecfg

		## Multiple server support, try until a working server found
		self.hosts = self.config["host"].split(",")
		self.serverIndex = 0

		## Check if the host can connect to ipv6 addresses
		## Some machines have the ipv6 support but can't connec to
		## ipv6 addresses and getaddrinfo returns the ipv6 address for them
		## for some reason, so we implemented a hack to test if the host machine
		## really can connect to ipv6 addresses... Feel free to improve ;)
		if syscmd.ipv6Connectivity( self ):
			self.socketType = socket.AF_UNSPEC
		else:
			self.socketType = socket.AF_INET

		## Initialize databases
		if "fmi" in mLoaded and not os.path.exists("modules/data/fmiCities.db"):
			self.errormsg = "[NOTICE] Cities database doesn't exist, creating it!"
			sysErrorLog.log( self )
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("blue"),self.errormsg,self.color("end")))
			syscmd.createCitiesDatabase( self )

		if "automodes" in mLoaded and not os.path.exists("modules/data/automodes.db"):
			self.errormsg = "[NOTICE] Automodes database doesn't exist, creating it!"
			sysErrorLog.log ( self )
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("blue"),self.errormsg,self.color("end")))
			syscmd.createAutomodesDatabase( self )

		if "seendb" in self.modulecfg["sysmodules"] and not os.path.exists(self.config["log-path"]+"seen.db"):
			self.errormsg = "[NOTICE] Seen Database doesn't exist, creating it!"
			sysErrorLog.log ( self )
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("blue"),self.errormsg,self.color("end")))
			syscmd.createSeenDatabase( self )

		if "tell" in mLoaded and not os.path.exists("modules/data/tell.db"):
			self.errormsg = "[NOTICE] Tell Database doesn't exist, creating it!"
			sysErrorLog.log ( self )
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("blue"),self.errormsg,self.color("end")))
			syscmd.createTellDatabase( self )
		
		self.loop()

	## COLOR CODES FOR BASH
	def color ( self, c ):
		if c == "red":
			return "\033[0;31m"	## RED
		if c == "green":
			return "\033[0;32m" ## GREEN
		if c == "blue":
			return "\033[0;34m" ## BLUE
		if c == "end":
			return "\033[0m"	## END 
		else:
			pass

	## Send data function
	def send_data( self, data ):
		try:
			## IRC Spec allows 512 chars in a msg including the \r\n
			##data = data[:510] + "\r\n"
			data = data + "\r\n"
			##print(len(data.encode("utf-8")))
			self.s.sendall( data.encode("utf-8") ) 
			print("[{0}] {1}"
				.format( time.strftime("%d.%m.%Y/%H:%M:%S"), data.rstrip("\r\n") ) )
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] send_data: {0}".format(e)		
			sysErrorLog.log( self ) ## LOG the error
			
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("red"), self.errormsg, self.color("end")))
				
	## Whois for getting userinfo (ident@hostname) [ RESERVED ONLY FOR AUTOMODES!!! ]
	def whois (self, nick):
		self.send_data("WHOIS {0}".format(nick))
		
	## Join channel
	def join_chan( self, chan ):
		self.send_data( "JOIN {0}".format(chan.strip()) )

	## Leave channel
	def part_chan( self, chan ):
		self.send_data( "PART {0} :See ya!".format(chan.strip()) )
		
	## Quit
	def quit( self ):
		self.send_data( "QUIT :Bye Bye!" )
		self.s.close()
		os._exit(1)
		
	## Send text to channel
	def send_chan( self, data ):
		## We don't want to send empty data
		if not data:
			return
		if len(self.msg) >= 3:	
			if len(data.encode("utf-8")) > 510:
				data = syscmd.split_utf8(self, data, 390)
				for line in data:
					msg = "PRIVMSG {0} :{1}".format(
						self.msg[2].strip().lstrip(":"), line.strip())
					self.send_data( msg )
					print( "Sending: {0}".format(msg) )
			else:
				msg = "PRIVMSG {0} :{1}".format(
					self.msg[2].strip().lstrip(":"), data.strip()) 
				self.send_data( msg )
				print( "Sending: {0}".format(msg) )
		else:
			return
		
	## Send a PM to the user doing a command
	def send_pm( self, data ):
		## We don't want to send empty data
		if not data:
			return
		msg = "PRIVMSG {0} :{1}".format(self.get_nick(), data.strip())
		self.send_data( msg )
		print( "Sending PM: {0}".format(msg) )
		
	## Send a NOTICE to the user doing a command
	def send_notice( self, data ):
		## We don't want to send empty data
		if not data:
			return
		msg = "NOTICE {0} :{1}".format(self.get_nick(), data.strip())
		self.send_data( msg )
		print( "Sending NOTICE: {0}".format(msg) )

	## Parse commands function
	def parse_command( self, cmd ):
		try:
			if cmd not in self.modulecfg["sysmodules"].split(",") and cmd in mLoaded:
				getattr(globals()[cmd], cmd)( self )
			else:
				self.send_chan( "Unknown command: !{0}".format( cmd ))
				return
		except AttributeError:
			self.send_chan( "Unknown command: !{0}".format( cmd ))
			return
			
	## Get nick
	def get_nick( self ):
		try:
			nick = re.search(":(.*)!", self.msg[0]).group(1)
			return(nick)
		except AttributeError:
			print( "Not a nick" )
	
	## Get user host
	def get_host( self ):
		try:
			host = self.msg[0].split("!")
			return(host[1])
		except:
			print( "Error getting host" )
	
	## Load a new module
	def load(self, module = None):
		if self.get_host() not in self.config["opers"]:
			return
		if len(self.msg) != 5:
			self.send_chan( "Usage: !load <module>" )
			return
		try:
			imp.reload(modulecfg)
			self.modulecfg = modulecfg.modulecfg
			if module in globals():
				self.send_chan("Module '{0}' is already loaded!".format(module))
			else:
				if module in self.modulecfg["modules"] or mod in self.modulecfg["sysmodules"]:
					globals()[module] = __import__(module)
					self.send_chan("Loaded a new module: {0}".format(module))
					mLoaded.append(module)
				else:
					self.send_chan("Unknown module: {0}".format(module))
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] load: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error	
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
					
	## Reload modules
	def reload( self ):
		if self.get_host() not in self.config["opers"]:
			return
		try:
			if len(self.msg) == 4: ## no parameters
				self.send_chan( "Usage: !reload <module> or !reload sys or !reload all" )
			command = self.msg[4].strip()
			if len(self.msg) == 5 and command == "all": ## Reload all user modules
				imp.reload(modulecfg)
				self.modulecfg = modulecfg.modulecfg
				for mod in self.modulecfg["modules"].split(","):
					print( "Reloading module {0}".format(mod) )
					imp.reload(globals()[mod])
				for mod in self.modulecfg["sysmodules"].split(","):
					print( "Reloading system module {0}".format(mod) )
					imp.reload(globals()[mod])
				self.send_chan("All modules and system modules reloaded!")
			if len(self.msg) == 5 and command == "sys": ## Reload all sys modules
				imp.reload(modulecfg)
				self.modulecfg = modulecfg.modulecfg
				for mod in self.modulecfg["sysmodules"].split(","):
					print( "Reloading system module {0}".format(mod) )
					imp.reload(globals()[mod])
				self.send_chan( "All system modules reloaded!" )
			if len(self.msg) == 5 and command != "all" and command != "sys": ## Reload specified module, if it exists
				if command in self.modulecfg["modules"]:
					imp.reload(modulecfg)
					self.modulecfg = modulecfg.modulecfg
					imp.reload(globals()[command])
					self.send_chan( "{0} module reloaded!".format(command) )
				else:
					self.send_chan("Unknown module: {0}".format(command))
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] reload: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

	## List available commands on the bot
	def cmd( self ):
		commands = ""
		for cmd in mLoaded:
			if cmd == "cobe":
				pass
			else:
				commands += "!{0} ".format(cmd)
		self.send_chan("Available commands: {0}".format(commands))
	
	## Restart the bot 
	def restart ( self ):
		if self.get_host() not in self.config["opers"]:
			return
		try:
			python = sys.executable
			self.send_data( "QUIT :Restarting!" )
			self.s.close()
			os.execl(python, python, * sys.argv)
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] restart: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			
			if self.config["debug"]:
				print("{0}{1}{2}"
					.format(self.color("red"), self.errormsg, self.color("end")))

	## Main loop, connect etc.
	def loop( self ):
	
		#IRC Codes (for logging/seendb)
		self.irc_codes = ["001", "002", "003", "004", "005", "042", "221", "251", "250", "252", "254",
				"255", "265", "266", "311", "312", "313", "317", "318", "319","332",
				"333","338","353", "366", "375", "372", "376", "401", "412", "433", "482","JOIN", "MODE", "PART"]

		self.errormsg = "" ## Set error messages to null
		self.connectionEstablished = 0
		
		if "cobe" in sys.modules:
			self.hal = cobe.brain.Brain("./cobe.brain")

		## Try until a working server has been found
		while self.connectionEstablished == 0:
			for res in socket.getaddrinfo(
				self.hosts[self.serverIndex], self.config["port"],
				self.socketType, socket.SOCK_STREAM ):

				af, socktype, proto, canonname, sa = res
			self.s = socket.socket( af, socktype, proto )
			try:
				print("{0}Conneting to {1}{2}"
					.format(pGreen, self.hosts[self.serverIndex], pEnd))
				self.s.connect(sa)
				self.connectionEstablished = 1
			except Exception as e:
				self.connectionEstablished = 0
				if self.serverIndex <= len(self.hosts):
					self.serverIndex += 1
				else:
					self.serverIndex = 0

				self.errormsg = "[ERROR]-[Core] Connection: {0}".format(e)
				sysErrorLog.log( self ) ## Log the error message in errorlog
				
				if self.config["debug"]:
					print("{0}{1}{2}"
						.format(self.color("red"), self.errormsg, self.color("end")))	

		self.nick = self.config["nick"]
		my_nick = "NICK {0}".format(self.nick)
		my_user = "USER {0} {1} pyTsunku :{2}".format(
			self.config["ident"], self.hosts[self.serverIndex], self.config["realname"])		

		## Send identification to the server
		self.send_data(my_nick)
		self.send_data(my_user)
		self.hostident = ""
		connected = 1
		logger = 0
		altnick = 1
		active = 0

		global flood
		
		while connected == 1:
			try:
				data = self.s.recv(512).decode( "utf-8", "ignore" )
				if len(data) == 0:
					connected == 0
					print( "Connection died, reconnecting" );
					time.sleep(5)
					self.loop()
			except Exception as e:
				connected == 0
				time.sleep(5)
				self.loop()
					
			self.msg = data.split(" ") ## Slice data into list

			## if debug is true, print some stuff	
			if self.config["debug"]:
				#print(self.msg)
				print("[{0}] {1}"
					.format( time.strftime("%d.%m.%Y/%H:%M:%S"), data ).rstrip("\r\n"))		

			if "ERROR" in self.msg[0] and ":Trying" in self.msg[1]: ## Sleep 20 secs if reconnecting too fast
				if self.config["debug"]:
					print("{0}[NOTICE] Trying to reconnect too fast, waiting for 20 second before trying again.{1}"
						.format(self.color("blue"), self.color("end")))
				time.sleep(20)
				self.loop()					
			
			##
			## AUTOMODES BELOW!!
			## Checks on JOIN event if user has an automode active
			##
			if len(self.msg) >= 2 and self.msg[1] == "JOIN":
				if self.get_nick() != self.nick:
					syscmd.modecheck(self)
					##
					## Including TELL module
					##
					if "tell" in mLoaded:
						tell.checkMessages(self)

			##
			## Built-in whois handler to get user ident@hostname from requested user
			## Only records ident@hostname if it was requested by automodes module
			## Line 311 marks the start of whois info from the server and later on 318 will end the whoise info
			##
			if len(self.msg) >= 2 and self.msg[1] == "311" and self.automodesWhoisEnabled:
				self.hostident = syscmd.getRemoteHost(self)
				##
				## Check the end of the whoise message and create the automode for the user
				##
				if "318" in self.msg:
					syscmd.addautomode(self,self.modes,self.channel)
					self.automodesWhoisEnabled == False
			##
			## Automodes END
			##

			## Logger
			if logger == 1:
				logger_daemon.logger_daemon( self )
				seendb.seendb( self ) #Seendb runs if logging is enabled

			## Check if user has a message in tell inbox
			if "tell" in mLoaded and len(self.msg) >= 4 and self.msg[1].strip() == "PRIVMSG" and self.msg[3][1:].strip() != "!tell":
				tell.checkMessages(self)

			## If someone sends PM to the bot, respond!
			if "366" in self.msg:
				active = 1
			try:
				if active == 1 and len(self.msg) >= 3:
					if self.msg[1] not in self.irc_codes and "Q!TheQBot@CServe.quakenet.org" not in self.msg[0]:
						if self.nick not in self.msg[0] and self.msg[2].strip() == self.nick:
							self.send_pm("I'm just a bot, don't waste your time")
			except IndexError:
				print("PM exception")
				pass
			
			## Support for Cobe (MegaHAL)
			if "cobe" in sys.modules:		
				if active == 1 and len(self.msg) >= 4 and "PRIVMSG" in self.msg[1]:
					if self.msg[1] not in self.irc_codes:
						phrase = ''
						length = len(self.msg)
						if self.nick not in self.msg[3] or ":Ichigo:" not in self.msg[3]:
							if self.nick in self.msg[3]:
								for x in range(4, length):
									phrase += "{0} ".format(self.msg[x])
							else:
								for x in range(3, length):
									phrase += "{0} ".format(self.msg[x])	
							self.hal.learn(phrase.strip().lstrip(":"))
						
						if self.nick.lower() in self.msg[3].lower() or self.nick in phrase:
							phrase = phrase.replace(self.nick, "")
							self.send_chan(self.hal.reply(phrase.strip().lstrip(":"), self.get_nick()))
				
			## PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG {0}".format(self.msg[1].strip()) )
				
			## Quakanet wants a pong reply on connect
			if "quakenet" in self.config["host"]:
				ping = data.split("\r\n")
				if len(ping) >= 2:
					pong = ping[1].split(" ")
					if pong[0] == "PING":
						self.send_data( "PONG {0}".format(pong[1].lstrip(":")) )		
						
			## Check if nick is in use, try alternative, if still in use, generate random number to the end of the nick
			try:
				if "433" in self.msg:
					if not altnick: # if altnick == 0
						print("Alternative nick in use, switching into random nick")
						self.nick = "{0}{1}".format(self.config["nick"], str(random.randrange(1,10+1)))
						my_nick = "NICK {0}".format(self.nick)
						self.send_data(my_nick)						
					else:
						print("Switching to the alternative nick")
						self.nick = self.config["altnick"]
						my_nick = "NICK {0}".format(self.nick)
						self.send_data(my_nick)
						altnick = 0 #if unable to set altnick, set altnick false and try random nick
						

			except IndexError:
				pass
			
			## If MOTD ended, everything is OK, so join the chans		
			if "376" in self.msg:
				chans = self.config["chans"].split(",")
				for chan in chans:
					self.join_chan( chan )
				if self.config["logging"]:
					logger = 1
					print( "{0}Logging enabled{1}".format(self.color("green"), self.color("end")) )
				else:
					print( "{0}Logging disabled{1}".format(self.color("red"), self.color("end")) )
						
			try:
				if len(self.msg) >= 4 and len(self.msg[3]) > 1:
					cmd = self.msg[3].lstrip(":").rstrip("\r\n")
					if cmd[0] == "!" and len(cmd) > 1:
						if cmd == "!load":
							try:
								self.load( self.msg[4].strip())
							except IndexError:
								self.load( None )
						elif cmd == "!cmd":
							self.cmd()
						elif cmd == "!reload":
							self.reload()
						elif cmd == "!join":
							if self.get_host() in self.config["opers"]:
								self.join_chan(self.msg[4])
						elif cmd == "!part":
							if self.get_host() in self.config["opers"]:
								self.part_chan(self.msg[4])
						elif cmd == "!quit":
							if self.get_host() in self.config["opers"]:
								self.quit()
						elif cmd == "!restart":
							self.restart()
						else:
							## Flood protection, add nick to the dictionary and raise the value by one every time he/she speaks
							if self.get_host() not in self.config["opers"] and self.get_nick() in flood:
								flood[self.get_nick()] += 1
							else:
								flood[self.get_nick()] = 1
							if flood[self.get_nick()] <= 3: ## If the nick has issued three commands before the timer is cleaned
								Thread(target=self.parse_command, args=(cmd.lstrip("!"),)).start() ## Run the commands in own threads, 
																						## so they won't block each other
							else:
								self.errormsg = "[NOTICE]-[Core] Flooding ({0})".format(self.get_host())
								sysErrorLog.log( self )
								print( "Flooding!" )
			except Exception as e:
				self.errormsg = "[ERROR]-[Core-Cmd] send_data: {0}".format(e)		
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"]:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
			
			## Get title for the URLs
			try:
				if len(self.msg) >= 4:
					if "372" not in self.msg and "332" not in self.msg and ":!isup" not in self.msg[3] and "TOPIC" not in self.msg[1]:
						urls = re.findall( '(?:[Hh]?[Tt]?[Tt]?[Pp])?(?:[sS]?)?://(?:[a-öA-Ö]|[0-9]|[$-_@.&+"®]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\w', data )
						if urls != None:
							for url in urls:
								## Run title as own thread so it won't block the bot
								Thread(target=title.title, args=(self, url)).start()
			except Exception as e:
				self.errormsg = "[ERROR]-[Core-Title] send_data: {0}".format(e)		
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"]:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## Clear flood counter; Clears the flood dictionary every x seconds
class Flood:
	def __init__( self ):
		global flood
		while True:
			#print(flood)
			flood = {}
			time.sleep(20)	


