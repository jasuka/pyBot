def op ( self ):
	self.send_data( "MODE " + self.msg[2] + " +o " + self.get_nick() )
