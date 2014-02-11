## Config
config = {		#[SERVER]			[Modify the right side only]
			#server settings
			"host":				"usa.b0xi.eu,b0xi.eu", 
			"port":				6667,
		
			#[BOT DETAILS]
			#Set bot details, chans etc..
			"nick":				"pyTsunku", 
			"altnick": 			"pyTunkio", 
			"realname":			"pyTsunku", 
			"ident":			"pyTsunku", 
			"chans":			"#tsunku",

			#[OPERS]
			#Bot operators
			"opers":			"hrna@oper.aquanet.fi,jaska@127.0.0.1",

			#[LOGGING DAEMON]
			#Loggin				
			"logging":					True,	#True/False, SeenDB works only if logging is set True

			"errLoglevel":					0, 	## Loglevels: 0, 1, 2
												## level 0 = no error logging
												## level 1 = logs the error
												## level 2 = logs the error with a backtrace

			"timeformat":				"%d.%m.%Y/%H:%M:%S", #[17.07.2013/13:31:27] do not to leave any space between date/time (at least for now)
			"TimestampBrackets":		"[,]",
			"log-path":					"logs/", #The root folder for logs
			
			#[DEV DEBUGGING]
			#Bot debugging true/false
			"debug":			True
				
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


