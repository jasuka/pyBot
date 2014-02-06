import urllib.parse
from bs4 import BeautifulSoup
import re
import os
import syscmd
import sys_error_log
import sqlite3

def fmi( self ):

	## For saving the city
	if len(self.msg) == 6:
		if "set" in self.msg:
			city = self.msg[5]
			setCity( self, city )
			self.send_notice( "Your city {0} has been saved!".format(city.title().strip()))
	else:
		try:
			if len(self.msg) == 4:	## when called only with !fmi, see if the city is saved
				city = getCity( self )
				if not city and len(self.msg) == 5:
					city = self.msg[4]
			if len(self.msg) == 5:
				city = self.msg[4].strip() #With !fmi City
			## If no city saved and no parameter
			if not city:
				self.send_chan( "Usage: !fmi <city> | !fmi set <city>" )
				return
		except IndexError:
			self.send_chan( "Usage: !fmi <city> | !fmi set <city>" )
			raise
			
		if "set" not in city and syscmd.checkCity( self, city ): # We don't want to look for a city named "set"
			
			city = city.title().strip()
			parameter = urllib.parse.quote(city)
			url = "http://ilmatieteenlaitos.fi/saa/" + parameter
			
			if city == "Oulu":
				url = "http://ilmatieteenlaitos.fi/saa/" + parameter + "?&station=101799"
			if city == "Helsinki":
				url = "http://ilmatieteenlaitos.fi/saa/" + parameter + "?&station=100971"
			if city == "Kilpisjärvi":
				url = "http://ilmatieteenlaitos.fi/saa/enonteki%C3%B6/" + parameter
	
			html = syscmd.getHtml(self, url, True )
 
			try:
				soup = BeautifulSoup(html)
				text = ""
				## When the weather was updated
				time = soup.find_all("span", class_="time-stamp")
				time = time[0].string.split(" ")
				time = time[1][:-7]

				str = soup.findAll("span", {"class" : "parameter-name-value"})
	   
				## Loop the reusts into a string
				for a in str:
					text += "{0} - ".format(a)
	   
				## Remove the Html tags	
				trimmed = syscmd.delHtml(text)

				output = "{0} klo {1}: {2}".format(city.strip(), time, trimmed)
				self.send_chan( output )
			except Except as e:
				self.errormsg = "[ERROR]-[fmi] fmi() stating: {0}".format(e)
				sys_error_log.log( self ) ## LOG the error
				if self.config["debug"] == "true":
					print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		else:
			self.send_chan( "City {0} doesn't exist!".format(city.title().strip()) )
			

## Return saved city for the nick
def getCity ( self ):

	nick = self.get_nick()
	try:
		db = sqlite3.connect("modules/data/fmiCities.db")

		cursor = db.cursor()

		## Check if the city is saved in the db
		cursor.execute("""
				SELECT city FROM nicks WHERE nick=? 
				""", (nick.strip(),))
		try:
			city = cursor.fetchone()[0]
		except TypeError:
			city = None
		return(city)
	except Exception as e:
		db.rollback()
		self.errormsg = "[ERROR]-[fmi] getCity() stating: {0}".format(e)
		sys_error_log.log() ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e
	finally:
		db.close()

## Save user city					
def setCity ( self, city ):

	nick = self.get_nick()
	city = city.title().strip()

	try:
		db = sqlite3.connect("modules/data/fmiCities.db")

		cursor = db.cursor()

		## Check if nick is in the db
		cursor.execute("""
				SELECT id FROM nicks WHERE nick=? 
				""", (nick.strip(),))
		try:
			nickId = cursor.fetchone()[0]
		except TypeError:
			nickId = None
		## If a nick is found, update the row
		if nickId:
			cursor.execute("""
					UPDATE nicks SET city=? WHERE id=? 
					""", (city, nickId))
			db.commit()
			return(True)
		## If not found, insert it
		else:
			cursor.execute("""
					INSERT INTO nicks(nick, city) VALUES(?, ?)  
					""", (nick.strip(), city))
			db.commit()
			return(True)			
	except Exception as e:
		db.rollback()
		self.errormsg = "[ERROR]-[fmi] setCity() stating: {0}".format(e)
		sys_error_log.log() ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e
	finally:
		db.close()

