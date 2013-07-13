#!/usr/bin/python

## Importataan tarvittavat modulet (socket, ?)
import socket
import time
## Class pyBot
class pyBot:
	def __init__( self ):
## Config

		self.config = {"host": "b0xi.eu", "port": 6667, "nick": "pyTsunku", "altnick": "pyTsunku2", "realname": "pyTsunku", 
					   "ident": "pyTsunku", "version": "pyBot version 0.1"}
		self.config["chans"] = "#tsunku"
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	## Connect (create socket, send userinfo)

	def connect( self ):
		nick = "NICK: %s\r\n" % self.config["nick"]
		user = "USER: %s %s pyTsunku :%s\r\n" % (self.config["ident"], self.config["host"], self.config["realname"])
		chan = "join %s\r\n" % self.config["chans"]
		self.socket.connect(( self.config["host"], self.config["port"]))
		print(self.socket.sendall(bytes(nick)))
		print(self.socket.sendall(bytes(user)))
		print(self.socket.sendall(bytes(user)))

	
	## Send data function
	#def send_data( data ):
	#	return(true)
		
	## Send text to channel function
	def send_chan( data ):
		return(true)
		
	## Send text as PRIVMSG
	def send_pm( data ):
		return(true)
		
	## Parse commands function
	def parse_command( command ):
		return(true)
		
	def loop( self ):

		while True:
			data = self.socket.recv(256)
			if len(data) == 0:
				break;
			msg = data.split(" ")
			print(msg[1])
			print(msg[2])
			if msg[0] == "PING":
				self.socket.sendall("PONG %s" % msg[1])
				
			print(data)
				
## Create new instance, execute connect function, enter the main loop
bot = pyBot()
bot.connect()
bot.loop()
