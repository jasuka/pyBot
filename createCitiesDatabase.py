#!/usr/bin/env python3

import sqlite3

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
	db = sqlite3.connect("modules/data/cities.db")

	cursor = db.cursor()

	## Drop the table if it exists
	cursor.execute("""
			DROP TABLE cities
			""")
	## Create cities table
	cursor.execute("""
			CREATE TABLE IF NOT EXISTS cities(id INTEGERT PRIMARY KEY, city TEXT)
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
	print("Done!")

