
##Simple stats version 1
import readline

def stats( self ):
	if self.config["logging"] == True:	#Logging must be enabled from config to run this module
		if self.msg[4].strip():
			if len(self.msg) >= 5:

				chan 	= self.msg[2]
				logfile = self.config["log-path"]+chan+".log"
				looking = self.msg[4].strip().rstrip("\r\n")
			
	
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

					for x in line:
						line2 = x.split(" ")
						logNick = line2[2].rstrip("\r\n").strip()
						
						if looking in line2:
							if looking != logNick:
								word_counter += 1
								print(line2)
						elif looking == logNick:
							nick_counter += 1

					if nick_counter is not 0:
						self.send_chan(looking+" has written '"+str(nick_counter)+"' lines on this channel ("+chan+")")
					elif word_counter is not 0:
						self.send_chan(looking+" is mentioned on '"+str(word_counter)+"' lines on this channel ("+chan+")")
					else:
						self.send_chan("I don't remember seeing '"+looking+"' on this channel before ("+chan+")")
			else:
				self.send_chan("Usage: !stats <nick> or !stats <word>")	#if not enough parameters, give away the usage
		else:
			self.send_chan("Received a whitespace as a search string, aborting")
	else:
		self.send_chan("First enable logging from config to use this module")
		
