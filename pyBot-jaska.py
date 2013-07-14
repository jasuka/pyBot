#!/usr/local/bin/python3

## Import needed modules
import socket
import re
import random
import sys
import time

## Config
import configjaska
## Bot functions
from modules import klo
from modules import title
from modules import op
from modules import version
from modules import fmi

## Class pyBot
class pyBot:
	def __init__( self ):
		
		## Config and start the bot
		self.config = configjaska.config
		self.loop()
			
	## Send data function
	def send_data( self, data ):
		data += "\r\n"
		self.s.sendall( data.encode("utf-8") ) 
		print( data )
			
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
		#try:
			getattr(globals()[cmd], cmd)( self )
		#except:
		#	self.send_chan( "Unknown command: !" + cmd )
	
	## Get nick
	def get_nick( self ):
		nick = re.search(":(.*)!", self.msg[0]).group(1)
		return(nick)
	
	## Main loop, connect etc.	
	def loop( self ):
	
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "pyTsunku :" + self.config["realname"]
		
		## ipv4/ipv6 support
		for res in socket.getaddrinfo( self.config["host"], self.config["port"], socket.AF_UNSPEC, socket.SOCK_STREAM ):
			af, socktype, proto, canonname, sa = res
		
		self.s = socket.socket( af, socktype, proto )
		
		try:
			self.s.connect(sa)
		except socket.error as msg:
			s.close()
			print("Could not open socket")
		
		## Send identification to the server
		self.send_data( nick )
		self.send_data( user )
		connected = 1
		
		while connected == 1:
			data = self.s.recv(4096).decode("utf-8")
			if len(data) == 0:
				connected == 0
				print("Connection died, reconnecting");
				time.sleep(2)
				self.loop()

			self.msg = data.split(" ") ## Slice data into list
			
			## PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG " + self.msg[1] )
			
			## Check if nick is in use, try alternative, if still in use, generate random number to the end of the nick
			try:
				if self.msg[7] == "433":
					self.send_data( "NICK " + self.config["altnick"] )
					if self.msg[7] == "433":
						self.send_data( "NICK " + self.config["nick"] + str(random.randrange(1,10+1)) )
			except IndexError:
				pass
			
			## If MOTD ended, everything is OK, so join the chans		
			if "376" in self.msg:
				chans = self.config["chans"].split(",")
				for chan in chans:
					self.join_chan( chan )
						
			try:
				cmd = self.msg[3].rstrip("\r\n")
				cmd = cmd.lstrip(":")
				if cmd[0] == "!":
					cmd = cmd.lstrip("!") ## remove ! from the command before parsing it
					self.parse_command( cmd )
			except IndexError:
				pass ## No need to do anything
			
			## Get title for the URLs
			
			try:
				url = re.search( "(http)(s)?:\/\/[a-zA-Z0-9\-\=.?&_/]+", data ).group(0)

				if url != None:
					title.title( self, url )
			except:
				pass
					
			## if debug is true, print some stuff	
			if self.config["debug"] == "true":
				#print(self.msg)
				print(data)
				
## Run the bot
try:
	bot = pyBot()
except KeyboardInterrupt:
	print("Ctrl+C Pressed, Quitting")
	