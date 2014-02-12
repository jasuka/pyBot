#seendb version 2
import re, time, os
import sysErrorLog
import sqlite3

def seendb ( self ):

	if os.path.exists(self.config["log-path"]) == True: #Checking if log-path in config is valid and exists (path is generated in logger_daemon.py)
		
		if len(self.msg) >= 4:	#Recording only if server sends more than 5 parameters (0,1,2,3,4,5) etc...
			if self.msg[1] in self.irc_codes or "NOTICE" in self.msg[1] or "MODE" in self.msg[1]:	#do nothing if server sends any of these parameters
				return
			else:
				try:
					seendb = self.config["log-path"]+"seen.db"
					timestamp = int(time.time())
					nick = self.get_nick()
					chan = self.msg[2].strip()
					usertxt = ""

					for i in range(3, len(self.msg)):
						usertxt += "{0} ".format(self.msg[i])

					#usertxt = re.sub(r'\\n|\\r|\\t','', usertxt)
					usertxt = usertxt[1:]
					
					db = sqlite3.connect(seendb)
					cur = db.cursor()

					cur.execute("""SELECT id FROM seendb WHERE nick = ?""",(nick,))
					try:
						resultId = cur.fetchone()[0]
					except TypeError:
						resultId = None

					if resultId:
						cur.execute("""UPDATE seendb SET channel = ?,time = ?, usertxt = ? WHERE id = ?""",(chan,timestamp,usertxt,resultId))
						db.commit()
					else:
						cur.execute("""INSERT INTO seendb(nick,channel,time,usertxt) VALUES(?,?,?,?)""",(nick,chan,timestamp,usertxt))
						db.commit()

				except Exception as e:
					self.errormsg = "[ERROR]-[seendb] seendb() stating: {0}".format(e)
					sysErrorLog.log( self ) ## LOG the error
					if self.config["debug"] == True:
						print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))	

				finally:
					db.close()