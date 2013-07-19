
##Simple stats version 1
import readline

def stats( self ):
	if self.config["logging"] == True:
		if len(self.msg) >= 4:

			chan = self.msg[2]
			logfile = self.config["log-path"]+chan+".log"

			try:
				with open(logfile): pass	#trying if such logfile exists or not
			except IOError:				#But yet i dont know, if this is a useless checkup
				self.send_chan("I think i have not been loggin on that channel yet")

			else:	
			
				LookingNick = self.msg[4].rstrip("\r\n")
				counter = 0
				log = open(logfile, "r")
				line = log.readlines()
				log.close()

				for x in line:
					line2 = x.split(" ")
					if LookingNick in line2:
						counter += 1
			
				if counter is not 0:
					self.send_chan(LookingNick + " has written " + str(counter) + " lines on this channel ("+ chan +")")
				else:
					self.send_chan("I don't remember seeing "+ LookingNick +" on this channel before ("+ chan +")")
		
				return
		else:
			self.send_chan("Usage: !stats <nick>")
	else:
		self.send_chan("First enable logging from config to use this module")
		
