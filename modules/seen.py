import time
import datetime
import dateutil.relativedelta
from time import gmtime, strftime
import re
import sysErrorLog
import sqlite3
import os

def seen ( self ):
	
	if self.config["logging"] == True: 	#If logging is False, we cannot get results, so make sure it's on in order to have this on.
		if len(self.msg) >= 5:		#If given string is only !seen, it will print out the usage of the script
			try:
				seendb = self.config["log-path"]+"seen.db"	#making sure seen.db file exists
				os.path.exists(seendb)
			except Exception as e:
				self.errormsg = "[ERROR]-[seen] seen() stating: {0}".format(e)
				sysErrorLog.log( self ) ## LOG the error
				if self.config["debug"] == True:
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
			else:
				nick = self.msg[4].rstrip("\r\n") #getting the nick we are looking for (the second param. given; !seen nick)

				if self.get_nick() != nick:	#if you're not looking yourself, run the search, other wise not.
					if self.nick != nick:
						
						db = sqlite3.connect(seendb)
						cur = db.cursor()
						cur.execute("""SELECT nick, channel, time, usertxt FROM seendb WHERE nick = ?""",(nick,))
						result = cur.fetchone()

						if result:
							name = result[0]
							dbtime = result[2]
							dbconvert = datetime.datetime.fromtimestamp(int(dbtime)).strftime('[%d.%m.%Y // %H:%M:%S]')
							past = datetime.datetime.fromtimestamp(int(dbtime))
							current = datetime.datetime.fromtimestamp(int(time.time()))
							diff = dateutil.relativedelta.relativedelta(current, past)
							output = ""
									
							#Looking from filed database time if any of these conditions will meet and appending them in output

							if diff.years:
								output += " {0} year(s)".format(diff.years)
							if diff.months:
								output += " {0} months(s)".format(diff.months)
							if diff.weeks:
								output += " {0} months(s)".format(diff.weeks)
							if diff.days:
								output += " {0} day(s)".format(diff.days)
							if diff.hours:
								output += " {0} hour(s)".format(diff.hours)
							if diff.minutes:
								output += " {0} minute(s)".format(diff.minutes)
							if diff.seconds:
								output += " {0} seconds".format(diff.seconds)

							self.send_chan("{0} spoke last time: {1} which is exactly {2} ago. Stating: {3}".format(name, dbconvert, output, result[3]))
							
						else:
							self.send_chan("I have never logged {0} while being on any channel".format(nick))
					else:
						self.send_chan("Hah, you're funny :)")
				else:
					self.send_chan("Hah, nice try!")

		else:
			self.send_chan("Usage: !seen <nick>")
	else:
		self.send_chan("Logging must be enabled from config in order to use this module")
					
