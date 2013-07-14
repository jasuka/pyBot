#!/usr/bin/python3

import socket

##config##

import confighrna

##END of cfg##
class pyTsu:
	def __init__ ( self ):
		self.config = confighrna.config
		self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

	def connect ( self ):
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["nick"] + " " + self.config["host"] + " " + "BULLSHIT :" + self.config["realname"]
		self.s.connect(( self.config["host"], self.config["port"]
		self.send_data( nick )
		self.send_data( user )
		
	
	def send_data ( self, data ):
		data += "\r\n"
		self.s.sendall ( data.ecnode("UTF-8") )
		print data

	def loop ( self ):
		while True:
			print ("IM ALIVE")





bot = pyTsu()
bot.connect()
bot.loop()
