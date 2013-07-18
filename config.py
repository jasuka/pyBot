## Config
config = {		#[SERVER]			[Modify the right side only]
			#server settings
			"host":				"b0xi.eu", 
			"hostv6":			"2a00:7b80:3019:12::84e6:a83",
			"port":				6667,
			"ipv6":				"true", 
		
			#[BOT DETAILS]
			#Set bot details, chans etc..
			"nick":				"pyTsunku", 
			"altnick": 			"pyTunkio", 
			"realname":			"pyTsunku", 
			"ident":			"pyTsunku", 
			"version":			"pyBot version 0.2.3", 
			"chans":			"#tsunku",

			#[OPERS]
			#Bot operators
			"opers":			"hrna@oper.aquanet.fi,jaska@127.0.0.1",

			#[MODULES]
			#Modules & System modules, you better not touch system modules
			"sysmodules":			"syscmd,logger_daemon,title", #Do not touch this line!!
			"modules":			"cmd,clock,op,version,fmi,currency,hello,youtube,stats",

			#[LOGGING DAEMON]
			#Loggin
			"logging":			"true",
			"timeformat":			"%d.%m.%Y/%H:%M:%S", #[17.07.2013/13:31:27] do not to leave any space between date/time (at least for now)
			"TimestampBrackets":		"[,]",

			#[DEV DEBUGGING]
			#Bot debugging true/false
			"debug":			"true"
				
		  }
			#Everything is editable, but if you dont know what you're doing, dont touch anything else than bot details.
			#Below some help for setting timeformat:
			#%a	Locale’s abbreviated weekday name.	 
			#%A	Locale’s full weekday name.	 
			#%b	Locale’s abbreviated month name.	 
			#%B	Locale’s full month name.	 
			#%c	Locale’s appropriate date and time representation.	 
			#%d	Day of the month as a decimal number [01,31].	 
			#%H	Hour (24-hour clock) as a decimal number [00,23].	 
			#%I	Hour (12-hour clock) as a decimal number [01,12].	 
			#%j	Day of the year as a decimal number [001,366].	 
			#%m	Month as a decimal number [01,12].	 
			#%M	Minute as a decimal number [00,59].	 
			#%p	Locale’s equivalent of either AM or PM.	(1)
			#%S	Second as a decimal number [00,61].	(2)
			#%U	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53].
			#		All days in a new year preceding the first Sunday are considered to be in week 0.	(3)
			#%w	Weekday as a decimal number [0(Sunday),6].	 
			#%W	Week number of the year (Monday as the first day of the week) as a decimal number [00,53].
			#		All days in a new year preceding the first Monday are considered to be in week 0.	(3)
			#%x	Locale’s appropriate date representation.	 
			#%X	Locale’s appropriate time representation.	 
			#%y	Year without century as a decimal number [00,99].	 
			#%Y	Year with century as a decimal number.	 
			#%Z	Time zone name (no characters if no time zone exists).	 
			#%%	A literal '%' character.

