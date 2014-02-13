
##Simple stats version 2
try:
	import readline
except ImportError:
	import pyreadline as readline ## This is for windows
import sysErrorLog

def stats( self ):
	if self.config["logging"]:	#Logging must be enabled from config to run this module
		if len(self.msg) >= 5:		#if no atributes, give the usage.
			if self.msg[4].strip():	#prevent searching whitespaces

				chan 	= self.msg[2]
				logfile = self.config["log-path"]+chan+".log"
				looking = self.msg[4].lower().rstrip("\r\n")

				try:
					with open(logfile): pass	#trying if such logfile exists or not
				except IOError:				#But yet i dont know, if this is a useless checkup
					self.send_chan("I think i have not been loggin on that channel yet")

				try:
					#If no errors were occured, open the log file and read lines.
					log = open(logfile, "r")
					line = log.readlines()
					log.close()
					nick_counter = 0
					word_counter = 0
					line_counter = 0
					pct = 0

					for x in range(0, len(line)):				#reading every line individually
						line2 = line[x].lower().strip().split(" ")	#stripping the line and splitting it into list
						logNick = line2[1].lower().strip()		#the nick in log will be always the second in the list [1]
						line_counter += 1				#counts every line in the logfile
						if looking == logNick:				#if we are looking the nick, count it in here
							nick_counter += 1
						
						else:						#otherwise we will loop the list trough to search for the word
							for y in range(0, len(line2)):		#this kind of double looping might slow down the performance..?
								if looking in line2[y]:		#if we have a match, count it in.
									word_counter += 1
					
					if nick_counter is not 0:
						pct = nick_counter/line_counter*100
						self.send_chan("{0} has written '{1}' lines on this channel ({2}) which is {3:.1f}% of the total amount.".format(looking, nick_counter, chan, round(pct,1)))
					elif word_counter is not 0:
						word_counter -= 1
						self.send_chan("{0} has been mentioned '{1}' times on this channel ({2})".format(looking, word_counter, chan))
					else:
						self.send_chan("I don't remember seeing '{0}' on this channel before ({1})".format(looking, chan))
				except Exception as e:
					self.errormsg = "[ERROR]-[stats] stats() stating: {0}".format(e)
					sysErrorLog.log( self ) ## LOG the error
					if self.config["debug"]:
						print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
					
			else:
				self.send_chan("Received a whitespace as a search string, aborting") #if searching whitespaces, give an error
		else:
			self.send_chan("Usage: !stats <nick> or !stats <word>")	#if not enough parameters, give away the usage
	else:
		self.send_chan("First enable logging from config to use this module")
		
