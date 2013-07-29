
##Simple stats version 2
import readline

def stats( self ):
	if self.config["logging"] == True:	#Logging must be enabled from config to run this module
		if len(self.msg) >= 5:		#if no atributes, give the usage.
			if self.msg[4].strip():	#prevent searching whitespaces

				chan 	= self.msg[2]
				logfile = self.config["log-path"]+chan+".log"
				looking = self.msg[4].rstrip("\r\n")

				try:
					with open(logfile): pass	#trying if such logfile exists or not
				except IOError:				#But yet i dont know, if this is a useless checkup
					self.send_chan("I think i have not been loggin on that channel yet")

				else:
					log = open(logfile, "r")
					line = log.readlines()
					log.close()
					nick_counter = 0
					word_counter = 0

					for x in range(0, len(line)):
						line2 = line[x].strip().split(" ")
						logNick = line2[1].strip()
						
						if looking == logNick:
							nick_counter += 1
						
						else:
							if looking in line2:
								word_counter += 1
					
					if nick_counter is not 0:
						self.send_chan("{0} has written '{1}' lines on this channel ({2})".format(looking, nick_counter, chan))
					elif word_counter is not 0:
						word_counter -= 1
						self.send_chan("{0} is mentioned on '{1}' lines on this channel ({2})".format(looking, word_counter, chan))
					else:
						self.send_chan("I don't remember seeing '{0}' on this channel before ({1})".format(looking, chan))
			else:
				self.send_chan("Received a whitespace as a search string, aborting") #if searching whitespaces, give an error
		else:
			self.send_chan("Usage: !stats <nick> or !stats <word>")	#if not enough parameters, give away the usage
	else:
		self.send_chan("First enable logging from config to use this module")
		
