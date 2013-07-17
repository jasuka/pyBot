
##Simple stats version 1
import readline

def stats( self ):
	counter = 0
	try:
		chan = self.msg[2]

	except IndexError:
		print("Error, something is wrong :(\r\n")
	else:	
		
		LookingNick = self.msg[4].rstrip("\r\n")
		logfile = "logs/"+chan+".log"
		log = open(logfile, "r")
		line = log.readlines()
		log.close()

		for x in line:
			line2 = x.split(" ")
			if LookingNick in line2:
				counter += 1
			
		if counter is not False:
			self.send_chan(LookingNick + " has written " + str(counter) + " lines on this channel ("+ chan +")")
		else:
			self.send_chan("I don't remember seeing "+ LookingNick +" on this channel before ("+ chan +")")
		
		return
		
