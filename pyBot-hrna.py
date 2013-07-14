#!/usr/bin/python3

import socket

##config##

import confighrna

##END of cfg##
class pyTsu:
	def __init__ ( self ):
		self.config = confighrna.config
		self.loop()
	def send_data ( self, data ):
		data += "\r\n"
		self.s.sendall ( data.encode("UTF-8") )
		print (data)

	def join_channel ( self, chan ):
		self.send_data("JOIN "+ chan)
		

	def loop ( self ):
		self.s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		nick = "NICK " + self.config["nick"]
		user = "USER " + self.config["ident"] + " " + self.config["host"] + " " + "BULLSHIT :" + self.config["realname"]
		self.s.connect(( self.config["host"], self.config["port"] ))
		self.send_data( nick )
		self.send_data( user )

		while True:
			data = self.s.recv(4096).decode("UTF-8")
			self.msg = data.split(" ")

			if self.msg[0] == "PING":
				self.send_data(self.msg[1])

			
			if "376" in self.msg:
				self.join_channel(self.config["chans"])

				
			
			print(data)


bot = pyTsu()







