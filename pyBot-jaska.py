#!/usr/local/bin/python3

## Importataan tarvittavat modulet (socket, ?)
import socket
import re
from modules import klo_module

## Class pyBot
class pyBot:
	def __init__( self ):
## Config
	
		self.config = {"host": "b0xi.eu", "port": 6667, "nick": "pyTsunku", "altnick": "pyTsunku2", "realname": "pyTsunku", 
					   "ident": "pyTsunku", "version": "pyBot version 0.1", "debug": "true"}
		self.config["chans"] = "#tsunku"

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	## Connect and send required data to the server
	def connect( self ):
		
		nick = "NICK " + self.config["nick"]
		#user = "USER %s %s pyTsunku :%s" % (self.config["ident"], self.config["host"], self.config["realname"])
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "pyTsunku :" + self.config["realname"]
		chan = "JOIN " + self.config["chans"]
		self.s.connect(( self.config["host"], self.config["port"]))
		self.send_data(nick)
		self.send_data(user)
		self.send_data(chan)

	
	## Send data function
	def send_data( self, data ):
		data += "\r\n"
		self.s.sendall( data.encode("utf-8") ) 
		print( data )
			
	# Join function
	def join_chan( self, chan ):
		return(true)
		
	## Send text to channel function
	def send_chan( self, data ):
		msg = "PRIVMSG " + self.msg[2] + " :" + str(data)
		self.send_data( msg )
		print("Sending: " + msg)
		
	## Send text as PRIVMSG
	def send_pm( self, data ):
		return(true)
		
	## Parse commands function
	def parse_command( self, cmd ):
		try:
			a = cmd + "_module"
			getattr(globals()[a], cmd)( self, self.msg )
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
				print("Connection has died! :/")
				break;
			self.msg = data.split(" ")
			
			# PING PONG
			if self.msg[0] == "PING":
				self.send_data( "PONG " + self.msg[1] )
			
			try:
				cmd = self.msg[3].rstrip("\r\n")
				cmd = cmd.lstrip(":")
				if cmd[0] == "!":
					cmd = cmd.lstrip("!") #remove ! from the command before parsing it
					self.parse_command( cmd )
			except IndexError:
				print("")
				
			# if debug is true, print some stuff	
			if self.config["debug"] == "true":
				print( self.msg )	
				print(data)
				
## Create new instance, execute connect function, enter the main loop
bot = pyBot()
bot.connect()
try:
	bot.loop()
except KeyboardInterrupt:
	print("You pressed Ctrl+C!")
