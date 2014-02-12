## TELL versio 1
import sqlite3
import os
import sysErrorLog

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

			db = sqlite3.connect("modules/data/tell.db")
			cur = db.cursor()
			cur.execute("""INSERT INTO tell (nick, channel, message) VALUES (?, ?, ?)""",(nick,channel,message.strip("\r\n")))
			db.commit()

		except Exception as e:
			self.errormsg = "[ERROR]-[tell] tell() stating: {0}".format(e)
			sysErrorLog.log ( self )
			if self.config["debug"] == True:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		finally:
			db.close()

def checkMessages( self ):

	if self.msg[1].strip() is "JOIN":
		print("FUCK")
		db = sqlite3.connect("modules/data/tell.db")
		cur = db.cursor()
		cur.execute("""SELECT id, nick, channel, message FROM tell WHERE nick = ? AND channel = ?""",(self.get_nick(),self.msg[2][1:]))
		results = cur.fetchall()
		db.close()

		for result in results:
			if self.get_nick() is result[1] and self.msg[2][1:] is result[2]:
				self.send_chan("{0} you have got a new message: {1}".format(self.get_nick(),result[3]))






