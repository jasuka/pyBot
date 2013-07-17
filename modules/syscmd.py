###
#	System commands for the bot
#
##
## Send data function
def send_data( self, data ):
	data += "\r\n"
	self.s.sendall( data.encode("utf-8") ) 
	print( data )
		
## Join channel
def join_chan( self, chan ):
	self.send_data("JOIN " + chan)
	
## Send text to channel
def send_chan( self, data ):
	msg = "PRIVMSG " + self.msg[2] + " :" + str(data)
	self.send_data( msg )
	print("Sending: " + msg)
	
## Send a PM to the user doing a command
def send_pm( self, data ):
	msg = "PRIVMSG " + self.get_nick() + " :" +str(data)
	self.send_data( msg )
	print("Sending PM: " + msg)

## Parse commands function
def parse_command( self, cmd ):
	try:
		if cmd not in self.config["sysmodules"].split(","):
			getattr(globals()[cmd], cmd)( self )
		else:
			return
	except KeyError:
		self.send_chan( "Unknown command: !" + cmd )

## Get nick
def get_nick( self ):
	try:
		nick = re.search(":(.*)!", self.msg[0]).group(1)
		return(nick)
	except AttributeError:
		print("Not a nick\r\n")

## Get user host
def get_host( self ):
	try:
		host = self.msg[0].split("!")
		return(host[1])
	except:
		print("Error getting host\r\n")
	
## Reload modules
def reload( self ):
	if self.get_host() not in self.config["opers"]:
		return
	try:
		if len(self.msg) == 4: ## no parameters
			self.send_chan("Usage: !reload <module> or !reload all")
		command = self.msg[4].rstrip("\r\n").strip()
		if len(self.msg) == 5 and command == "all": ## Reload all modules
			imp.reload(config)
			self.config = config.config
			for mod in self.config["modules"].split(","):
				print("Reloading module {0}".format(mod))
				imp.reload(globals()[mod])
			self.send_chan("All modules reloaded!")
		if len(self.msg) == 5 and command != "all": ## Reload specified module, if it exists
			if command in self.config["modules"]:
				imp.reload(config)
				self.config = config.config
				imp.reload(globals()[command])
				self.send_chan("{0} module reloaded!".format(command))
			else:
				self.send_chan("Unknown module: {0}".format(command))
	except:
		raise