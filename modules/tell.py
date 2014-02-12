## TELL versio 1
import sqlite3
import os
import sysErrorLog

"""
TELL DB STRUCTURE IS AS FOLLOWS: (id INTEGER PRIMARY KEY NOT NULL, nick TEXT, who TEXT, channel TEXT, message TEXT)
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
				message += "{0} ".format(self.msg[i].strip())

			message = message.rstrip("\r\n")

			db = sqlite3.connect("modules/data/tell.db")
			cur = db.cursor()
			cur.execute("""INSERT INTO tell (nick, who, channel, message) VALUES (?, ?, ?, ?)""",(nick,self.get_nick(),channel,message))
			db.commit()
			self.send_chan("Your message has been saved")

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
		chan = self.msg[2].lstrip(":").strip()
		db = sqlite3.connect("modules/data/tell.db")
		cur = db.cursor()

		cur.execute("""SELECT * FROM tell WHERE nick = ? AND channel = ?""",(nick,chan))
		results = cur.fetchall()
		
		for row in results:
			if nick in row[1] and chan in row[3]:
				self.send_chan("{0}, {1} has sent you a message: {2}".format(nick, row[2] ,row[4]))
				cur.execute("""DELETE FROM tell WHERE id=?""",(row[0],))
			db.commit()	

	except Exception as e:
		self.errormsg = "[ERROR]-[tell] checkMessages() stating: {0}".format(e)
		sysErrorLog.log ( self )
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	finally:
		db.close()	




