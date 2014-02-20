## TELL versio 1
import sqlite3
import os
import sysErrorLog
import syscmd

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
			self.errormsg = "{0}[ERROR]-[tell] tell()(1): No database file found!{1}".format(self.color("red"),self.color("end"))
			sysErrorLog.log ( self )
			return

		try:
			## Get needed data from the stream
			nick = self.msg[4].strip()
			tellCount = self.config["tellCount"]-1
			userInbox = self.config["userInbox"]-1

			if self.get_nick() == nick or self.nick == nick:
				self.send_chan("This doesn't seem right now, does it?")
				return
				
			if self.msg[2][0] == "#":
				channel = self.msg[2]
			else:
				#Not valid channel, do nothing..
				return

			message = ""
			for i in range(5, len(self.msg)):
				message += "{0} ".format(self.msg[i].strip())

			message = message.rstrip("\r\n")

			if syscmd.userVisitedChannel( self, nick ):

				db = sqlite3.connect("modules/data/tell.db")
				cur = db.cursor()

				cur.execute("""SELECT COUNT(who) AS count FROM tell WHERE who = ?""",(self.get_nick(),))
				checkCount = cur.fetchone()[0]

				cur.execute("""SELECT COUNT(nick) AS count FROM tell WHERE nick = ?""",(nick,))
				checkInbox = cur.fetchone()[0]

				if checkCount > tellCount:
					self.send_chan("{0}, The message count is limited in to {1} messages per user"
						.format(self.get_nick(), tellCount+1))

				elif checkInbox > userInbox:
					self.send_chan("{0}, {1}'s message inbox is full :(".format(self.get_nick(), nick))

				else:
					cur.execute("""INSERT INTO tell (nick, who, channel, message) VALUES (?, ?, ?, ?)""",
						(nick,self.get_nick(),channel,message))
					db.commit()
					self.send_chan("Your message has been saved")

				db.close()
			else:
				self.send_chan("I cannot tell something to someone who doesn't exists :(")
				
		except Exception as e:
			self.errormsg = "[ERROR]-[tell] tell() stating: {0}".format(e)
			sysErrorLog.log ( self )
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))


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

		if results:
			msgToUser = "{0}, ".format(nick)
			for row in results:
				if nick in row[1] and chan in row[3]:
					msgToUser += "[{0} has sent you a message: {1}] ".format(row[2] ,row[4])
					cur.execute("""DELETE FROM tell WHERE id=?""",(row[0],))
				db.commit()	
			self.send_chan(msgToUser)
		else:
			return

		db.close()
	except Exception as e:
		self.errormsg = "[ERROR]-[tell] checkMessages() stating: {0}".format(e)
		sysErrorLog.log ( self )
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))






