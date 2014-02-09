import urllib.request
import os
import re
import time
import sysErrorLog
import socket
import sqlite3

### Create cities DB, feel free to edit the list of cities
def createCitiesDatabase():
	cities = """Akaa, Alahärmä, Alajärvi, Alastaro, Alastaro, Alavieska, Alavus, Anjala, Artjärvi, 
	Asikkala, Askainen, Askola, Aura, Auttoinen, Dragsfjärd, Ekenäs, Elimäki, Eno, Enonkoski, 
	Enontekiö, Espoo, Eura, Eurajoki, Evijärvi, Forssa, Haapajärvi, Haapavesi, Hailuoto, Halikko, 
	Halsua, Hamina, Hankasalmi, Hanko, Harjavalta, Hartola, Hauho, Haukipudas, Haukivuori, Hausjärvi, 
	Heinola, Heinävesi, Helsinki, Himanka, Hirvensalmi, Hollola, Honkajoki, Houtskär, Huittinen, Humppila, 
	Hyrynsalmi, Hyvinkää, Hämeenkoski, Hämeenkyrö, Hämeenlinna, Ii, Iisalmi, Iitti, Ikaalinen, Ilmajoki, 
	Ilomantsi, Imatra, Inari, Ingå, Iniö, Isojoki, Isokyrö, Ivalo, Jaala, Jakobstad, Jalasjärvi, Janakkala, 
	Joensuu, Jokioinen, Joroinen, Joutsa, Joutseno, Juankoski, Jurva, Juuka, Juupajoki, Juva, Jyväskylä, Jämijärvi, 
	Jämsä, Jämsänkoski, Jäppilä, Järvenpää, Kaarina, Kaavi, Kajaani, Kalajoki, Kalvola, Kangasala, Kangaslampi, 
	Kangasniemi, Kankaanpää, Kannonkoski, Kannus, Karhula, Karijoki, Karinainen, Karis, Karjalohja, Karkkila, 
	Karleby, Karstula, Karttula, Karvia, Karvia, Kaskinen, Kauhajoki, Kauhava, Kauniainen, Kaustinen, Keitele, 
	Kemi, Kemijärvi, Keminmaa, Kempele, Kerava, Kerimäki, Kestilä, Kesälahti, Keuruu, Kihniö, Kiihtelysvaara, 
	Kiikala, Kiikoinen, Kiiminki, Kilo, Kilpisjärvi, Kimito, Kinnula, Kinnula, Kirkkonummi, Kisko, Kitee, Kittilä, 
	Kiukainen, Kiuruvesi, Kivijärvi, Kokemäki, Kolari, Konnevesi, Kontiolahti, Korpilahti, Korsholm, Korsnäs, Kortesjärvi, 
	Koski, Kotka, Koukkuniemi, Kouvola, Kristinestad, Kronoby, Kuhmalahti, Kuhmo, Kuhmoinen, Kuivaniemi, Kullaa, Kuopio, 
	Kuortane, Kurikka, Kuru, Kuusamo, Kuusankoski, Kuusjoki, Kylmäkoski, Kyyjärvi, Kälviä, Kärkölä, Kärkölä, Kärsämäki, 
	Köyliö, Lahti, Laihia, Laitila, Lammi, Lapinjärvi, Lapinlahti, Lappajärvi, Lappeenranta, Lappi, Lapua, Larsmo, Laukaa, 
	Lavia, Lehtimäki, Leivonmäki, Lemi, Lempäälä, Lemu, Leppävirta, Lestijärvi, Lieksa, Lieto, Liljendal, Liminka, Liperi, 
	Lohja, Lohtaja, Loimaa, Loimaan Kunta, Loppi, Lovisa, Luhanka, Lumijoki, Luopioinen, Luumäki, Luvia, Längelmäki, 
	Länsi-Turunmaa, Maaninka, Malax, Marttila, Masku, Mellilä, Merijärvi, Merikarvia, Merimasku, Miehikkälä, Mietoinen, 
	Mikkeli, Mouhijärvi, Muhos, Muhos, Multia, Muonio, Muurame, Muurla, Mynämäki, Myrskylä, Mäntsälä, Mänttä, Mäntyharju, 
	Naantali, Nagu, Nakkila, Nastola, Nilsiä, Nivala, Nokia, Noormarkku, Nousiainen, Nurmes, Nurmijärvi, Nurmo, Nykarleby, 
	Oravais, Orimattila, Oripää, Orivesi, Otaniemi, Oulainen, Oulu, Oulunsalo, Outokumpu, Padasjoki, Paimio, Paltamo, Pargas, 
	Parikkala, Parkano, Pedersöre, Pelkosenniemi, Pello, Perho, Perniö, Pernå, Pertteli, Pertunmaa, Petäjävesi, 
	Pieksämäen Maalaiskunta, Pieksämäki, Pielavesi, Pihtipudas, Piikkiö, Piippola, Pirkkala, Pohja, Polvijärvi, Pomarkku, 
	Pori, Pornainen, Porvoo, Posio, Pudasjärvi, Pukkila, Pulkkila, Punkaharju, Punkalaidun, Puolanka, Puumala, Pyhtää, Pyhäjoki, 
	Pyhäjärvi, Pyhäjärvi, Pyhäntä, Pyhäranta, Pyhäselkä, Pylkönmäki, Pälkäne, Pöytyä, Raahe, Raisio, Rantasalmi, Rantsila, 
	Ranua, Rauma, Rautalampi, Rautavaara, Rautjärvi, Reisjärvi, Renko, Replot, Riihimäki, Ristiina, Ristijärvi, Ristinummi, 
	Rovaniemi, Ruokolahti, Ruotsinpyhtää, Ruovesi, Rusko, Ruukki, Rymättylä, Rääkkylä, Saari, Saarijärvi, Sahalahti, Salla, Salo, 
	Sammatti, Sauvo, Savitaipale, Savonlinna, Savonranta, Savukoski, Seinäjoki, Sibbo, Sievi, Siikainen, Siikajoki, Siilinjärvi, 
	Simo, Simo, Siuntio, Sodankylä, Soini, Somero, Sonkajärvi, Sotkamo, Sulkava, Sumiainen, Suodenniemi, Suolahti, Suomusjärvi, 
	Suomussalmi, Suonenjoki, Sysmä, Säkylä, Särkisalo, Säynätsalo, Taipalsaari, Taivalkoski, Taivassalo, Tammela, Tampere, 
	Tarvasjoki, Teekkarikylä, Tervakoski, Tervo, Tervola, Teuva, Tohmajärvi, Toholampi, Toijala, Toivakka, Tornio, Turku, 
	Tuulos, Tuupovaara, Tuusniemi, Tuusula, Tyrnävä, Töysä, Ullava, Ulvila, Urjala, Utajärvi, Utsjoki, Uurainen, Uusikaupunki, 
	Vaala, Vaasa, Vahto, Valkeakoski, Valkeala, Valtimo, Vammala, Vampula, Vantaa, Varkaus, Varpaisjärvi, Vehmaa, Vehmersalmi, 
	Velkua, Vesanto, Vesilahti, Veteli, Vieremä, Vihanti, Vihti, Viiala, Viitasaari, Viljakkala, Vilppula, Vimpeli, Virrat, 
	Virtasalmi, Vuolijoki, Vähäkyrö, Västanfjärd, Vörå, Yli-Ii, Ylihärmä, Ylikiiminki, Ylistaro, Ylitornio, Ylivieska, Ylämaa, 
	Yläne, Ylöjärvi, Ypäjä, Äetsä, Ähtäri, Äänekoski"""

	citiesList = cities.split(",")

	try:
		db = sqlite3.connect("modules/data/fmiCities.db")

		cursor = db.cursor()

		## Drop the table if it exists
		cursor.execute("""
				DROP TABLE IF EXISTS cities
				""")
		## Create cities table
		cursor.execute("""
				CREATE TABLE IF NOT EXISTS cities(id INTEGER PRIMARY KEY NOT NULL, city TEXT)
				""")
		## Create nicks table
		cursor.execute("""
				CREATE TABLE IF NOT EXISTS nicks(id INTEGER PRIMARY KEY NOT NULL, nick TEXT, city TEXT)
				""")
		## Loop through the cities and add them to the db
		for city in citiesList:
			cursor.execute("""
				INSERT INTO cities(city) VALUES (?)
				""", (city.strip(),))
		## Commit changes to the db
		db.commit()
	except Exception as e:
		## Roll back if some error occured
		db.rollback()
		self.errormsg = "[ERROR]-[syscmd] createCitiesDatabase() stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e
	finally:
		db.close()
		return True
## END

def createAutomodesDatabase():
	try:
		db = sqlite3.connect("modules/data/automodes.db")

		cursor = db.cursor()
		cursor.execute("""DROP TABLE IF EXISTS automodes""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS automodes(id INTEGER PRIMARY KEY NOT NULL, identhost TEXT, channel TEXT, mode TEXT)""")
		db.commit()
	except Exception as e:
		db.rollback()
		self.errormsg = "[ERROR]-[syscmd] createAutomodesDataBase() stating: {0}".format(e)
		sysErrorLog.log ( self )
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e
	finally:
		db.close()
		return True
## END

def createSeenDatabase( self ):
	try:
		db = sqlite3.connect(self.config["log-path"]+"seen.db")

		cursor = db.cursor()
		cursor.execute("""DROP TABLE IF EXISTS seendb""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS seendb(id INTEGER PRIMARY KEY NOT NULL, nick TEXT, channel TEXT, time TEXT, usertxt TEXT)""")
		db.commit()
	except Exception as e:
		db.rollback()
		self.errormsg = "[ERROR]-[syscmd] createSeenDataBase() stating: {0}".format(e)
		sysErrorLog.log ( self )
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e
	finally:
		db.close()
		return True
## END

## Get HTML for given url
def getHtml( self, url, useragent):
	try:
		if useragent == True:
			user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
			headers = { 'User-Agent' : user_agent }
			req = urllib.request.Request(url, None, headers)
		else:
			req = urllib.request.Request(url, None)

		html = urllib.request.urlopen(req, timeout = 20).read()
		return(html)
	except Exception as e:
		self.errormsg = "[ERROR]-[syscmd] getHtml() stating: {0}".format(e)
		sysErrorLog.log ( self ) ## LOG the error
		self.send_chan( "~ {0}".format(e))
## End

## Check if the city exists in Finland
def checkCity ( self, city ):

	try:
		db = sqlite3.connect("modules/data/fmiCities.db")

		cursor = db.cursor()

		## Check if the city is in the db
		cursor.execute("""
				SELECT city FROM cities WHERE city=? 
				""", (city.title().strip(),))
		if cursor.fetchone():
			return True
		else:
			return False
	except Exception as e:
		## Roll back if some error occured
		db.rollback()
		raise e
	finally:
		db.close()

## End

## Clears html tags from a string
def delHtml( html ):
	try:
		html = re.sub('<[^<]+?>', '', html)
		return(html)
	except Exception as e:
		self.errormsg = "[ERROR]-[syscmd] delHtml() stating: {0}".format(e)
		sysErrorLog.log() ## LOG the error
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))

## End

## Automodes checkup on event JOIN
def modecheck (self):
	try:
		db = sqlite3.connect("modules/data/automodes.db")
		cursor = db.cursor()
		cursor.execute("""SELECT identhost, channel, mode FROM automodes WHERE identhost = ? """,(self.get_host(),))
		result = cursor.fetchone()

		if result and result[1] in self.msg[2].lstrip(":"):
			if result[2] == "av":
				self.send_data("MODE {0} +v {1}".format(result[1], self.get_nick()))
			else:
				self.send_data("MODE {0} +o {1}".format(result[1], self.get_nick()))
	except Exception as e:
		self.errormsg = "[ERROR]-[syscmd] modecheck() stating: {0}".format(e)
		sysErrorLog.log (self)
		if self.config["debug"] == True:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
		raise e

## End

## ADD AUTOMODE
def addautomode (self,modes,chan):
	
	identhost = self.hostident.strip() 	#this is created by getRemoteHost() down below which is later on called
					   					#in core as a bot wide variable when server sends whoise code 311

	if modes == "ao" or modes == "av":
		try:
			db = sqlite3.connect("modules/data/automodes.db")
			cursor = db.cursor()
			cursor.execute("""SELECT id FROM automodes WHERE identhost = ?""", (identhost,))
			try:
				rowId = cursor.fetchone()[0]
			except TypeError:
				rowId = None
			if not rowId:
				cursor.execute("""INSERT INTO automodes(identhost,channel,mode) VALUES(?,?,?)""", (identhost,chan,modes))
				db.commit()
				self.send_data("PRIVMSG {2} :Automode ({0}) added for {1} on channel {2}".format(modes,identhost,chan))
				return True
			else:
				cursor.execute("""UPDATE automodes SET mode = ? WHERE id = ?""", (modes, rowId))
				db.commit()
				self.send_data("PRIVMSG {2} :Automode changed for {1} on channel {2}. The new mode is ({0})".format(modes,identhost,chan))
				return True
		except Exception as e:
			self.errormsg = "[ERROR]-[syscmd] addautomode() stating: {0}".format(e)
			sysErrorLog (self)
			if self.config["debug"] == True:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
			raise e
		finally:
			db.close()
	else:
		self.send_data("PRIVMSG {0} :Currently the only user flags are 'ao' & 'av'".format(chan))
## END


## Check if the currency is in the correct currencies list

def checkCurrency( frm, to ):
	currenciesList = ['ED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'ARY', 'AUD', 'AWG', 
			'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB','BOP',
			'BRC', 'BRL', 'BSD', 'BTN', 'BWP', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF',
			'CLP', 'CNY', 'COP', 'CRC', 'CSK', 'CUP', 'CVE', 'CYP', 'CZK','DJF', 'DKK',
			'DOP', 'DZD', 'ECS', 'EEK', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP',
			'GEL', 'GHC', 'GIP', 'GMD', 'GNF', 'GTQ', 'GWP', 'GYD','HKD', 'HNL', 'HRK',
			'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK','JMD', 'JOD', 'JPY',
			'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD','KZT', 'LAK', 'LBP',
			'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL','MGA', 'MGF', 'MKD',
			'MMK', 'MNT', 'MOP', 'MRO', 'MTL', 'MUR', 'MVR', 'MWK', 'MXN','MXP', 'MYR',
			'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN','PGK',
			'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'ROL', 'RON', 'RSD', 'RUB', 'RWF', 'SAR',
			'SBD', 'SCR', 'SDD', 'SEK', 'SGD', 'SHP', 'SIT', 'SKK', 'SLL', 'SOS', 'SRD',
			'STD','SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMM', 'TND', 'TOP', 'TRL', 'TRY',
			'TTD', 'TWD', 'TZS','UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEB', 'VND', 'VUV',
			'WST', 'XAF', 'XBC', 'XCD', 'XFO', 'XOF', 'XPF', 'YER', 'YUM', 'ZAR', 'ZMK',
			'ZRN', 'ZWD']
			
	if frm.strip() in currenciesList and to.strip() in currenciesList:
		return(True)
	else:
		return(False)
## End

## Check if a given shortened lang is correct
def checkLang( lang ):
	langList = ['en', 'nl', 'de', 'fr', 'sv', 'it', 'es', 'ru', 'pl', 'ja', 'vi', 'pt',
			'zh', 'uk', 'ceb', 'war', 'ca', 'no', 'fi', 'fa', 'cs', 'hu', 'ko', 'ar',
			'ro', 'ms', 'tr', 'id', 'kk', 'sr', 'sk', 'eo', 'da', 'lt', 'eu', 'bg', 'he',
			'hr', 'sl', 'uz', 'vo', 'et', 'hi', 'nn', 'gl', 'simple', 'az', 'la', 'el',
			'oc', 'sh', 'th', 'ka', 'mk', 'new', 'pms', 'tl', 'be', 'ta', 'ht', 'te', 'be-x-old',
			'lv', 'cy', 'hy', 'bs', 'br', 'sq', 'tt', 'jv', 'mg', 'mr', 'lb', 'is', 'my', 'ml',
			'ba', 'yo', 'an', 'lmo', 'af', 'fy', 'pnb', 'bn', 'sw', 'bpy', 'io', 'ky', 'ur', 'ne',
			'zh-yue', 'scn', 'gu', 'nds', 'ga', 'ku', 'cv', 'ast', 'qu', 'su', 'sco', 'als', 'ia',
			'nap', 'bug', 'bat-smg', 'kn', 'map-bms', 'wa', 'am', 'ckb', 'gd', 'hif', 'zh-min-nan',
			'tg', 'arz', 'mzn', 'yi', 'vec', 'mn', 'sah', 'nah', 'roa-tara', 'sa', 'os', 'pam', 'si',
			'hsb', 'bar', 'se', 'li', 'mi', 'pa', 'co', 'fo', 'ilo', 'gan', 'bo', 'glk', 'rue', 'bcl',
			'min', 'fiu-vro', 'mrj', 'nds-nl', 'tk', 'ps', 'vls', 'xmf', 'gv', 'diq', 'or', 'kv', 'pag',
			'zea', 'km', 'dv', 'mhr', 'nrm', 'csb', 'frr', 'rm', 'koi', 'vep', 'udm', 'lad', 'lij', 'wuu',
			'fur', 'sc', 'zh-classical', 'ug', 'stq', 'mt', 'ay', 'pi', 'so', 'bh', 'ce', 'ksh', 'nov',
			'hak', 'kw', 'ang', 'pcd', 'nv', 'gn', 'as', 'ext', 'frp', 'ace', 'szl', 'eml', 'gag', 'ie',
			'ln', 'krc', 'pfl', 'xal', 'haw', 'pdc', 'rw', 'crh', 'to', 'dsb', 'kl', 'arc', 'lez', 'myv',
			'kab', 'sn', 'bjn', 'pap', 'tpi', 'lbe', 'wo', 'mwl', 'jbo', 'mdf', 'kbd', 'cbk-zam', 'av',
			'srn', 'ty', 'lo', 'ab', 'kg', 'tet', 'ltg', 'na', 'ig', 'bxr', 'nso', 'za', 'kaa', 'zu',
			'chy', 'rmy', 'cu', 'tn', 'chr', 'roa-rup', 'cdo', 'bi', 'got', 'sm', 'mo', 'bm', 'iu', 'pih',
			'pnt', 'ss', 'sd', 'ki', 'ee', 'ha', 'om', 'fj', 'ti', 'ts', 'ks', 've', 'sg', 'rn', 'st', 'cr', 
			'dz', 'ak', 'tum', 'lg', 'ff', 'ik', 'ny', 'tw', 'ch', 'xh', 'ng', 'ii', 'cho', 'mh', 'aa', 'kj', 
			'ho', 'mus', 'kr', 'hz']

	if lang.strip() in langList:
		return(True)
	else:
		return(False)
## END

## Return remote host based on given nick

def getRemoteHost (self):
	#print("{0}@{1}".format(self.msg[4],self.msg[5]))
	hostident = "{0}@{1}".format(self.msg[4],self.msg[5])
	return(hostident)
## End

## Replace umlauts 
def replaceUmlauts(text):
	dic = {'Ä':'%C3%84', 'ä':'%C3%A4', 'Ö':'%C3%96', 'ö':'%C3%B6', '"':'%22', '®':'%C2%AE'}
	for i, j in dic.items():
		text = text.replace(i, j)
	return text

## Can the host connect to ipv6 hosts
def ipv6Connectivity():
	have_ipv6 = True
	s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	try:
		s.connect(('2a00:1450:400f:802::1000', 0)) ## google.com ipv6 address
	except:
		have_ipv6 = False
	return have_ipv6

## Split UTF-8 s into chunks of maximum length n.
def split_utf8(self, s, n):
	while len(s) > n:
		k = n
		while (ord(s[k]) & 0xc0) == 0x80:
			k -= 1
		yield s[:k]
		s = s[k:]
	yield s
