def op ( self ):
	try:
		self.send_data( "MODE " + self.msg[2] + " +o " + self.msg[4] )
	except IndexError:
		self.send_data( "MODE " + self.msg[2] + " +o " + self.get_nick() )
	
