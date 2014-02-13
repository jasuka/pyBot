## TELL versio 1
import sqlite3
import os
import sysErrorLog
import syscmd

"""
TELL DB STRUCTURE IS AS FOLLOWS: (id INTEGER PRIMARY KEY NOT NULL, nick TEXT, channel TEXT, message TEXT)
"""

def tell( self ):

	if len(self.msg) <= 4:
		self.send_chan("Usage: !tell <nick> <message>")
		return
	else:
		## Gotta check if the file realy exists
		if not os.path.exists("modules/data/tell.db"):
			## ERRORII TÄHÄ !!
			return
		try:
			## Get needed data from the stream
			nick = self.msg[4].strip()

			if self.msg[2][0] is "#":
				channel = self.msg[2]
			else:
				## ERRORI
				return

			message = ""
			for i in range(5, len(self.msg)):
				message += "{0} ".format(self.msg[i])

			message = message.rstrip("\r\n")

			if syscmd.userVisitedChannel( self, nick ):
				db = sqlite3.connect("modules/data/tell.db")
				cur = db.cursor()
				cur.execute("""INSERT INTO tell (nick, channel, message) VALUES (?, ?, ?)""",(nick,channel,message))
				db.commit()
				self.send_chan("Your message has been saved")
			else:
				self.send_chan("I cannot tell something to someone who doesn't exists :(")
				return

		except Exception as e:
			self.errormsg = "[ERROR]-[tell] tell() stating: {0}".format(e)
			sysErrorLog.log ( self )
			if self.config["debug"] == True:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		finally:
			db.close()

def checkMessages( self ):
	if not os.path.exists("modules/data/tell.db"):
		## ERRORII TÄHÄ !!
		return
	try:
		nick = self.get_nick()
		chan = self.msg[2][1:]

		db = sqlite3.connect("modules/data/tell.db")
		cur = db.cursor()

		cur.execute("""SELECT * FROM tell WHERE nick = ? AND channel = ?""",(nick,chan))
		print(cur.fetchall())
		
		#print(results)
		for result in cur.fetchall():
			if self.get_nick() is result[1] and self.msg[2][1:] is result[2]:
				self.send_chan("{0} you have got a new message: {1}".format(self.get_nick(),result[3]))

	except Exception as e:
		self.errormsg = "[ERROR]-[tell] checkMessages() stating: {0}".format(e)
		sysErrorLog.log ( self )
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	finally:
		db.close()	




