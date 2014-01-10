#!/usr/bin/env python3

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

sys.path.insert(0, './modules') ## Path for the modules

## Import Config
import config
## Import modules config
import modulecfg
## Load modules from the modules config
try:
	for mod in modulecfg.modulecfg["sysmodules"].split(","):
		print("Loading system module {0}".format(mod))
		globals()[mod] = __import__(mod)
	for mod in modulecfg.modulecfg["modules"].split(","):
		print("Loading module {0}".format(mod))
		globals()[mod] = __import__(mod)
except (ImportError, SyntaxError) as e:
	print("Couldn't load module: {0}".format(mod))
	if config.config["debug"] == "true":
		print(e)
	pass
except Exception as e:
	if config.config["debug"] == "true":
		print("[ERROR]-[Core] Load modules: {0} , This error is not being logged".format(e))

## Global variable for the flood protection
flood = {}

## Class pyBot
class pyBot():
	def __init__( self ):
	
	## Bot Version
		self.version = "pyBot version 0.6.4"
	## Config and start the bot
		self.config = config.config
		self.modulecfg = modulecfg.modulecfg
		self.loop()
			
	## Send data function
	def send_data( self, data ):
		try:
			## IRC Spec allows 512 chars in a msg including the \r\n
			data = data[:510] + "\r\n"
			self.s.sendall( data.encode("utf-8") ) 
			print("[{0}] {1}".format( time.strftime("%d.%m.%Y/%H:%M:%S"), data ) )
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] send_data: {0}".format(e)		
			sys_error_log.log( self ) ## LOG the error
			
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] send_data: {0}".format(e))
				
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
		msg = "PRIVMSG {0} :{1}".format(self.msg[2], data.strip())
		self.send_data( msg )
		print( "Sending: {0}\r\n".format(msg) )
		
	## Send a PM to the user doing a command
	def send_pm( self, data ):
		msg = "PRIVMSG {0} :{1}".format(self.get_nick(), data.strip())
		self.send_data( msg )
		print( "Sending PM: {0}\r\n".format(msg) )
		
	## Send a NOTICE to the user doing a command
	def send_notice( self, data ):
		msg = "NOTICE {0} :{1}".format(self.get_nick(), data.strip())
		self.send_data( msg )
		print( "Sending NOTICE: {0}\r\n".format(msg) )

	## Parse commands function
	def parse_command( self, cmd ):
		try:
			if cmd not in self.modulecfg["sysmodules"].split(","):
				getattr(globals()[cmd], cmd)( self )
			else:
				return
		except KeyError:
			self.send_chan( "Unknown command: {0}!".format( cmd ))
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] parse_command: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] parse_command: {0}".format(e))
	
	## Get nick
	def get_nick( self ):
		try:
			nick = re.search(":(.*)!", self.msg[0]).group(1)
			return(nick)
		except AttributeError:
			print( "Not a nick\r\n" )
	
	## Get user host
	def get_host( self ):
		try:
			host = self.msg[0].split("!")
			return(host[1])
		except:
			print( "Error getting host\r\n" )
	
	## Load a new module
	def load(self, module = None):
		if self.get_host() not in self.config["opers"]:
			return
		try:
			mod = ""
			if len(self.msg) == 5 and module == None:
					mod = self.msg[4].strip()
			if module != None:
					mod = module
			if len(mod) > 0:
				imp.reload(modulecfg)
				self.modulecfg = modulecfg.modulecfg
				if mod in globals():
					self.send_chan("Module '{0}' is already loaded!".format(mod))
				else:
					if mod in self.modulecfg["modules"] or mod in self.modulecfg["sysmodules"]:
						globals()[mod] = __import__(mod)
						self.send_chan("Loaded a new module: {0}".format(mod))
					else:
						self.send_chan("Unknown module: {0}".format(mod))
			else:
				self.send_chan( "Usage: !load <module>" )
		except Exception as e:
			self.errormsg = "[ERROR]-[Core] load: {0}".fomat(e)
			sys_error_log.log( self ) ## LOG the error
			
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] load: {0}".fomat(e))
					
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
			sys_error_log.log( self ) ## LOG the error
			
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] reload: {0}".format(e))
	
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
			sys_error_log.log( self ) ## LOG the error
			
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] restart: {0}".format(e))

	## Main loop, connect etc.
	def loop( self ):
	
		#IRC Codes (for logging/seendb)
		self.irc_codes = ["001", "002", "003", "004", "005", "042", "251", "250", "252", "254", 
				"255", "265", "266", "311", "312", "313", "317", "318", "319","332",
				"333","338","353", "366", "375", "372", "376", "401", "433", "482","JOIN"]
		self.errormsg = "" ## Set error messages to null
		
		self.nick = self.config["nick"]
		my_nick = "NICK {0}".format(self.nick)
		my_user = "USER {0} {1} pyTsunku :{2}".format(self.config["ident"], self.config["host"], self.config["realname"])
		
		## ipv4/ipv6 support
		for res in socket.getaddrinfo( self.config["host"], self.config["port"], socket.AF_UNSPEC, socket.SOCK_STREAM ):
			af, socktype, proto, canonname, sa = res
		self.s = socket.socket( af, socktype, proto )
		try:
			self.s.connect(sa)
		except Exception as e:
		
			self.errormsg = "[ERROR]-[Core] Connection: {0}".format(e)
			sys_error_log.log( self ) ## Log the error message in errorlog
			
			if e.errno == 101:
				self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
				self.s.connect(( self.config["host"], self.config["port"] ))
			if self.config["debug"] == "true":
				print("[ERROR]-[Core] Connection: {0}".format(e))	

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
					print( "Connection died, reconnecting\r\n" );
					time.sleep(5)
					self.loop()
			except Exception as e:
				connected == 0
				if "ERROR :Trying to reconnect too fast." in data: ## Sleep 15 secs if reconnecting too fast
					time.sleep(20)
				else:
					time.sleep(5)
					self.loop()
					
			self.msg = data.split(" ") ## Slice data into list
			
			## if debug is true, print some stuff	
			if self.config["debug"] == "true":
				#print(self.msg)
				print("[{0}] {1}".format( time.strftime("%d.%m.%Y/%H:%M:%S"), data ))							
			
			## AUTOMODES BELOW!!
			if self.msg[1] == "JOIN":
				if self.get_nick() != self.nick:
					syscmd.modecheck(self)
			## built-in whois handler to get user ident@hostname from requested user [ IF using self.whois in any purpose, it will run trough this.. ]
			if self.msg[1] == "311":
				self.hostident = syscmd.getRemoteHost(self)
			if "318" in self.msg: ##a Quick fix, gotta rethink it over if having time anytime...
				syscmd.addautomode(self,self.modes,self.channel)
			## End of Automodes fix ... should be fixed if any better ideas...

			## Logger
			if logger == 1:
				logger_daemon.logger_daemon( self )
				seendb.seendb( self ) #Seendb runs if logging is enabled
			
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
				
			## PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG {0}".format(self.msg[1].strip()) )
				
			## Quakanet wants a pong reply on connect
			if "quakenet" in self.config["host"]:
				ping = data.split("\r\n")
				pong = ping[1].split(" ")
				if pong[0] == "PING":
					self.send_data( "PONG {0}".format(pong[1].lstrip(":")) )		
						
			## Check if nick is in use, try alternative, if still in use, generate random number to the end of the nick
			try:
				if "433" in self.msg:
					if altnick is 0:
						print("Alternative nick in use, switching into random nick\r\n")
						self.nick = "{0}{1}".format(self.config["nick"], str(random.randrange(1,10+1)))
						my_nick = "NICK {0}".format(self.nick)
						self.send_data(my_nick)						
					else:
						print("Switching to the alternative nick\r\n")
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
				if self.config["logging"] == True:
					logger = 1
					print( "Logging enabled\r\n" )
				else:
					print( "Logging disabled\r\n" )
						
			try:
				if len(self.msg) >= 4:
					cmd = self.msg[3].lstrip(":").rstrip("\r\n")
					if cmd[0] == "!" and len(cmd) > 1:
						if cmd == "!load":
							self.load()
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
							if self.get_nick() in flood:
								flood[self.get_nick()] += 1
							else:
								flood[self.get_nick()] = 1
							if flood[self.get_nick()] <= 3: ## If the nick has issued three commands before the timer is cleaned
								Thread(target=self.parse_command, args=(cmd.lstrip("!"),)).start() ## Run the commands in own threads, 
																						## so they won't block each other
							else:
								self.errormsg = "[NOTICE]-[Core] Flooding ({0})".format(self.get_host())
								sys_error_log.log( self )
								print( "Flooding!\r\n" )
			except IndexError:
				print("Cmd exception")
				pass ## No need to do anything
			
			## Get title for the URLs
			try:
				if len(self.msg) >= 4:
					if "372" not in self.msg and "332" not in self.msg and ":!isup" not in self.msg[3] and "TOPIC" not in self.msg[1]:
						urls = re.findall( 'http[s]?://(?:[a-öA-Ö]|[0-9]|[$-_@.&+"®]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data )
						if urls != None:
							for url in urls:
								## Run title as own thread so it won't block the bot
								Thread(target=title.title, args=(self, url)).start()
			except Exception as e:
				if self.config["debug"] == "true":
					print("URL Title exception")
					print(e)

## Clear flood counter; Clears the flood dictionary every x seconds
class Flood:
	def __init__( self ):
		global flood
		while True:
			#print(flood)
			flood = {}
			time.sleep(20)	

## Run the bot and flood counter in own threads
def initialize():
	bot = Thread(target=pyBot)
	fld = Thread(target=Flood)

	bot.daemon = True
	bot.start()
	fld.daemon = True
	fld.start()
	while True: ## Keep the main thread alive
		time.sleep(1)
try:
	initialize()
except Exception:
	self.errormsg("[ERROR]-[Core] Connection failure, attempting to reconnect")
	sys_error_log.log( self ) ## LOG the error
	initialize()	
except KeyboardInterrupt:
	#os._exit(1)
	print( "Ctrl+C, Quitting!\r\n" )

