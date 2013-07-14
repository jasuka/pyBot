def op ( self, data ):
	self.send_data( "MODE " + data[2] + "+o " + get_nick( data ) )
