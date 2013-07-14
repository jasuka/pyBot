#!/usr/bin/python3

import socket

##config##

import confighrna

##END of cfg##
class pyTsu:
	def __init__ ( self ):
		self.config = confighrna.config
	
	def send_data ( self, data ):
		data += "\r\n"
		self.s.sendall ( data.ecnode("UTF-8") )
		print (data)
		

	def loop ( self ):
		self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "BULLSHIT :" + self.config["realname"]
		self.s.connect(( self.config["host"], self.config["port"]
		self.send_data( nick )
		self.send_data( user )

		while True:
			data = self.s.recv(4096).decode("UTF-8")


bot = byTsu()
bot.loop()






