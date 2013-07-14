#!/usr/bin/python3

import socket

##config##

import confighrna
import time
import re
from modules import klo

##END of cfg##
class pyTsu:
	def __init__ ( self ):
		self.config = confighrna.config
		self.loop()

	def send_data ( self, data ):
		data += "\r\n"
		self.s.sendall ( data.encode("UTF-8") )
		print (data)

	def get_nick( self ):
		nick = re.search(":(.*)!", self.msg[0]).group(1)
		return(nick)

	def join_chan ( self, chan ):
		self.send_data("JOIN "+ chan)
	
	def send_chan ( self, data ):
		msg = "PRIVMSG " + self.msg[2] + " :" + str(data)
		self.send_data(msg)
		

	def parse_command( self, cmd ):
		try:
			getattr(globals()[cmd], cmd)( self )
		except:
			self.send_chan( "Unknown command: !" + cmd )
		

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
				self.join_chan(self.config["chans"])

				
			if self.config["debug"] == "true":
				print (data)

			try:
				cmd = self.msg[3].rstrip("\r\n")
				cmd = cmd.lstrip(":")
				if cmd[0] == "!":
					cmd = cmd.lstrip("!") ## remove ! from the command before parsing it
					self.parse_command( cmd )

			except IndexError:
				pass ## No need to do anything


bot = pyTsu()







