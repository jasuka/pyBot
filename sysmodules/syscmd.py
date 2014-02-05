import urllib.request
import os
import re
import time
import sys_error_log
import socket
import sqlite3

## Create cities DB, feel free to edit the list of cities
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
		db = sqlite3.connect("sysmodules/data/cities.db")

		cursor = db.cursor()

		## Drop the table if it exists
		cursor.execute("""
				DROP TABLE IF EXISTS cities
				""")
		## Create cities table
		cursor.execute("""
				CREATE TABLE IF NOT EXISTS cities(id INTEGERT PRIMARY KEY, city TEXT)
				""")
		## Create nicks table
		cursor.execute("""
				CREATE TABLE IF NOT EXISTS nicks(id INTEGERT PRIMARY KEY, nick TEXT, city TEXT)
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
		sys_error_log.log ( self ) ## LOG the error
		self.send_chan( "~ {0}".format(e))
## End

## Check if the city exists in Finland
def checkCity ( self, city ):

	if not os.path.exists("sysmodules/data/cities.db"):
		if self.config["debug"] == "true":
			print("{0}[NOTICE] Cities database doesn't exist, creating it!{1}".format(self.color("blue"), self.color("end")))
		createCitiesDatabase()
	try:
		db = sqlite3.connect("modules/data/cities.db")

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
		sys_error_log.log() ## LOG the error
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
			
## End

## Automodes checkup on event JOIN
def modecheck (self):
	file = "modules/data/automodes.txt"
	line2 = ""
	try:
		with open(file, "r", encoding="UTF-8") as modes:
			for line in modes:
				spl = line.split(";")
				#print(spl[0])
				line2 += spl[0]+","
			#line2 = line2.join(",")
			#print(line2)
			if self.get_host() in line2 and spl[2].strip() in self.msg[2].lstrip(":"):
				if spl[1].strip() == "ao":
					self.send_data("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
					print("MODE {0} +o {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
				elif spl[1].strip() == "av":
					self.send_data("MODE {0} +v {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
					print("MODE {0} +v {1}".format(spl[2].rstrip("\r\n"),self.get_nick()))
			#line2 = ""
	except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
		open(file, "a").close()
		self.errormsg = "[NOTICE]-[syscmd] modcheck(): Creating file for automodes '{0}'".format(file)
		sys_error_log.log ( self )
		if self.config["debug"] == "true":
			print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))

## End

## ADD AUTOMODE
def addautomode (self,modes,chan):
	
	identhost = self.hostident.strip() 	#this is created by getRemoteHost() down below which is later on called
					   	#in core as a bot wide variable when server sends whoise code 311
	file = "modules/data/automodes.txt"

	if modes == "ao" or modes == "av":
		try:
			if re.search("\\b"+identhost+";\\b", open(file).read(), flags=re.IGNORECASE):
				with open("modules/data/temp1.txt", "w", encoding="UTF-8") as temp:
					for line in open(file):				
						str = "{0};{1};{2}".format(identhost,modes,chan)
						temp.write(re.sub("^{0};.*$".format(identhost), str, line))
					os.remove("modules/data/automodes.txt")
					os.rename("modules/data/temp1.txt", file)
				self.send_data("PRIVMSG {2} :Automode changed for {1} on channel {2}. The new mode is ({0})".format(modes,identhost,chan))
				return(True)
			## If the nick doesn't exist in the file, append it in there
			else:
				with open(file, "a", encoding="UTF-8") as file:
					str = "\r\n{0};{1};{2}".format(identhost,modes,chan)
					file.write(str)
				self.send_data("PRIVMSG {2} :Automode ({0}) added for {1} on channel {2}".format(modes,identhost,chan))
				return(True)

		except (OSError, IOError):	#if it happens, the database file doesn't exist, create one
			open(file, "a").close()
			self.errormsg = "[NOTICE]-[syscmd] addautomode(): Creating file for automodes '{0}'".format(file)
			sys_error_log.log( self )
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("blue"), self.errormsg, self.color("end")))
		except Exception as e:
			self.errormsg = "[ERROR]-[syscmd] addautomode() stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	else:
		self.send_data("PRIVMSG {0} :Currently the only user flags are 'ao' & 'av'".format(chan))
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
