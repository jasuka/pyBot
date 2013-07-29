def op ( self ):
	try:
		if self.get_host() in self.config["opers"]:
			self.send_data("MODE {0} +o {1}".format(self.msg[2], self.msg[4]))
		else: 
			self.send_chan("Unauthorized command")
	except IndexError:
		if self.get_host() in self.config["opers"]:		
			self.send_data("MODE {0} +o {1}".format(self.msg[2], self.get_nick()))
		else:
			self.send_chan("Unauhtorized command")
