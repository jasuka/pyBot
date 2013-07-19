#!/usr/bin/env python3

## Import needed modules
import socket
import re
import random
import sys
import time
import importlib
import imp
from threading import Thread

sys.path.insert(0, './modules') ## Path for the modules

## Config
import config
## Load modules from the config
try:
	for mod in config.config["sysmodules"].split(","):
		print("Loading system module {0}".format(mod))
		globals()[mod] = __import__(mod)
	for mod in config.config["modules"].split(","):
		print("Loading module {0}".format(mod))
		globals()[mod] = __import__(mod)
except:
	raise

## Global variable for the flood protection
flood = {}

## Class pyBot
class pyBot():
	def __init__( self ):

	## Config and start the bot
		self.config = config.config
		self.loop()
			
	## Send data function
	def send_data( self, data ):
		data += "\r\n"
		self.s.sendall( data.encode("utf-8") ) 
		print("[{0}] {1}".format( time.strftime("%d.%m.%Y/%H:%M:%S"), data ))
			
	## Join channel
	def join_chan( self, chan ):
		self.send_data("JOIN " + chan)
		
	## Send text to channel
	def send_chan( self, data ):
		msg = "PRIVMSG " + self.msg[2] + " :" + str(data)
		self.send_data( msg )
		print("Sending: " + msg)
		
	## Send a PM to the user doing a command
	def send_pm( self, data ):
		msg = "PRIVMSG " + self.get_nick() + " :" +str(data)
		self.send_data( msg )
		print("Sending PM: " + msg)

	## Parse commands function
	def parse_command( self, cmd ):
		try:
			if cmd not in self.config["sysmodules"].split(","):
				getattr(globals()[cmd], cmd)( self )
			else:
				return
		except KeyError:
			self.send_chan( "Unknown command: !" + cmd )
	
	## Get nick
	def get_nick( self ):
		try:
			nick = re.search(":(.*)!", self.msg[0]).group(1)
			return(nick)
		except AttributeError:
			print("Not a nick\r\n")
	
	## Get user host
	def get_host( self ):
		try:
			host = self.msg[0].split("!")
			return(host[1])
		except:
			print("Error getting host\r\n")
		
	## Reload modules
	def reload( self ):
		if self.get_host() not in self.config["opers"]:
			return
		try:
			if len(self.msg) == 4: ## no parameters
				self.send_chan("Usage: !reload <module> or !reload all")
			command = self.msg[4].rstrip("\r\n").strip()
			if len(self.msg) == 5 and command == "all": ## Reload all user modules
				imp.reload(config)
				self.config = config.config
				for mod in self.config["modules"].split(","):
					print("Reloading module {0}".format(mod))
					imp.reload(globals()[mod])
			if len(self.msg) == 5 and command == "sys": ## Reload all sys modules
				imp.reload(config)
				self.config = config.config
				for mod in self.config["sysmodules"].split(","):
					print("Reloading system module {0}".format(mod))
					imp.reload(globals()[mod])
				self.send_chan("All system modules reloaded!")
			if len(self.msg) == 5 and command != "all" and command != "sys": ## Reload specified module, if it exists
				if command in self.config["modules"]:
					imp.reload(config)
					self.config = config.config
					imp.reload(globals()[command])
					self.send_chan("{0} module reloaded!".format(command))
				else:
					self.send_chan("Unknown module: {0}".format(command))
		except:
			raise
	
	## Main loop, connect etc.	
	def loop( self ):
	
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "pyTsunku :" + self.config["realname"]
		
		if self.config["ipv6"] == "true":
			## ipv4/ipv6 support
			for res in socket.getaddrinfo( self.config["hostv6"], self.config["port"], socket.AF_UNSPEC, socket.SOCK_STREAM ):
				af, socktype, proto, canonname, sa = res
			self.s = socket.socket( af, socktype, proto )
			try:
				self.s.connect(sa)
			except socket.error as msg:
				s.close()
				print("Could not open socket")
		else:
			try:
				self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
				self.s.connect(( self.config["host"], self.config["port"] )) 
			except socket.error as msg:
				s.close()
				print("Could not open socket")
		
		## Send identification to the server
		self.send_data( nick )
		self.send_data( user )
		connected = 1
		logger = 0
		altnick = 1
		global flood
		
		while connected == 1:
			try:
				data = self.s.recv(4096).decode("utf-8", "ignore")
				if len(data) == 0:
					connected == 0
					print("Connection died, reconnecting\r\n");
					time.sleep(5)
					self.loop()
			except ConnectionResetError as msg:
				connected == 0
				if "ERROR :Trying to reconnect too fast." in data: ## Sleep 15 secs if reconnecting too fast
					time.sleep(15)
				else:
					time.sleep(5)
					self.loop()
					
			self.msg = data.split(" ") ## Slice data into list
			
			## if debug is true, print some stuff	
			if self.config["debug"] == "true":
				#print(self.msg)
				print("[{0}] {1}".format( time.strftime("%d.%m.%Y/%H:%M:%S"), data ))								

			## Logger
			if logger == 1:
				logger_daemon.logger_daemon( self )
			
			## PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG " + self.msg[1] )
				
			## Quakanet wants a pong reply on connect
			if "quakenet" in self.config["host"]:
				ping = data.split("\r\n")
				pong = ping[1].split(" ")
				if pong[0] == "PING":
					self.send_data( "PONG " + pong[1].lstrip(":"))		
						
			## Check if nick is in use, try alternative, if still in use, generate random number to the end of the nick
			try:
				if "433" in self.msg:
					if altnick is 0:
						self.send_data( "NICK " + self.config["nick"] + str(random.randrange(1,10+1)) )
					else:
						self.send_data( "NICK " + self.config["altnick"] )
						altnick = 0 #if unable to set altnick, set altnick false and try random nick
						print("Alternative nick in use, switching into random nick\r\n")

			except IndexError:
				pass
			
			## If MOTD ended, everything is OK, so join the chans		
			if "376" in self.msg:
				chans = self.config["chans"].split(",")
				for chan in chans:
					self.join_chan( chan )
				if self.config["logging"] == True:
					logger = 1
					print("Logging enabled\r\n")
				else:
					print("Logging disabled\r\n")
						
			try:
				cmd = self.msg[3].rstrip("\r\n")
				cmd = cmd.lstrip(":")
				if cmd[0] == "!":
					if cmd == "!reload":
						self.reload( )
					else:
						## Flood protection, add nick to the dictionary and raise the value by one every time he/she speaks
						if self.get_nick() in flood:
							flood[self.get_nick()] += 1
						else:
							flood[self.get_nick()] = 1
						if flood[self.get_nick()] <= 3: ## If the nick has issued three commands before the timer is cleaned
							cmd = cmd.lstrip("!") ## remove ! from the command before parsing it
							self.parse_command( cmd )
						else:
							print("Flooding!")
			except IndexError:
				pass ## No need to do anything
			
			## Get title for the URLs
			try:
				if "372" not in self.msg and "332" not in self.msg:
					url = re.search( "(Http|http)(s)?:\/\/[a-zA-Z0-9\-\=.?&_/]+", data ).group(0)
					if url != None:
						title.title( self, url )
			except:
				pass

## Clear flood counter; Clears the flood dictionary every x seconds
class Flood:
	def __init__( self ):
		global flood
		while True:
			#print(flood)
			flood = {}
			time.sleep(20)	

## Run the bot and flood counter in own threads
try:
	bot = Thread(target=pyBot)
	flood = Thread(target=Flood)

	bot.daemon = True
	bot.start()
	flood.daemon = True
	flood.start()
	while True: ## Keep the main thread alive
		time.sleep(1)		
except KeyboardInterrupt:
	sys.exit(1)
	print("Ctrl+C, Quitting!")

