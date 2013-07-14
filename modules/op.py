def op ( self ):
	if self.msg[4] == False:
		self.send_data( "MODE " + self.msg[2] + " +o " + self.get_nick() )
	else:
		self.send_data( "MODE " + self.msg[2] + " +o " + self.msg[4] )
