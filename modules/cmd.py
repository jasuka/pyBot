
def cmd( self ):

	commands = ""
	for cmd in self.config["modules"].split(","):
		commands += "!{0} ".format(cmd)
		
	self.send_chan("Available commands: {0}".format(commands))