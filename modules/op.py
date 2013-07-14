def op ( self ):
	try:
		if self.get_nick() in self.config["opers"]:
			self.send_data( "MODE " + self.msg[2] + " +o " + self.msg[4] )
		else: 
			self.send_chan("Unauthorized command")
	except IndexError:
		if self.get_nick() in self.config["opers"]:		
			self.send_data( "MODE " + self.msg[2] + " +o " + self.get_nick() )
		else:
			self.send_chan("Unauhtorized command")
