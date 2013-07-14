#!/usr/local/bin/python3

## Importataan tarvittavat modulet (socket, ?)
import socket
import re
import random
import sys

#config
import configjaska
#modules
from modules import klo

## Class pyBot
class pyBot:
	def __init__( self ):
	
		self.config = configjaska.config
		#Socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	## Connect and send required data to the server
	def connect( self ):
		
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "pyTsunku :" + self.config["realname"]
		#chan = "JOIN " + self.config["chans"]
		self.s.connect(( self.config["host"], self.config["port"]))
		self.send_data( nick )
		self.send_data( user )
			
	## Send data function
	def send_data( self, data ):
		data += "\r\n"
		self.s.sendall( data.encode("utf-8") ) 
		print( data )
			
	# Join channel
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
			getattr(globals()[cmd], cmd)( self, self.msg )
		except:
			self.send_chan( "Unknown command: !" + cmd )
	
	## Get nick
	def get_nick( self ):
		nick = re.search(":(.*)!", self.msg[0]).group(1)
		return(nick)
		
	def loop( self ):

		while True:
			data = self.s.recv(4096).decode("utf-8")
			if len(data) == 0:
				self.s.close()
				sys.exit()
				break
				
			self.msg = data.split(" ")
			
			# PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG " + self.msg[1] )
			
			# Check if nick is in use, try alternative, if still in use, generate random number to the end of the nick
			try:
				if self.msg[7] == "433":
					print("Täällä ollaan")
					self.send_data( "NICK " + self.config["altnick"] )
					if self.msg[7] == "433":
						self.send_data( "NICK " + self.config["nick"] + str(random.randrange(1,10+1)) )
			except IndexError:
				pass
			
			# If MOTD ended, join the chans		
			if "376" in self.msg:
				chans = self.config["chans"].split(",")
				for chan in chans:
					self.join_chan( chan )
						
			try:
				cmd = self.msg[3].rstrip("\r\n")
				cmd = cmd.lstrip(":")
				if cmd[0] == "!":
					cmd = cmd.lstrip("!") #remove ! from the command before parsing it
					self.parse_command( cmd )
			except IndexError:
				pass # No need to do anything
				
			# if debug is true, print some stuff	
			if self.config["debug"] == "true":
				#print(self.msg)
				print(data)
				
## Create new instance, execute connect function, enter the main loop
try:
	bot = pyBot()
	bot.connect()
	bot.loop()
except KeyboardInterrupt:
	print("Ctrl+C Pressed, quitting")
except SystemExit:
	bot = pyBot()
	bot.connect()
	bot.loop()
