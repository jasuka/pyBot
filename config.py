## Config
config = {		#[SERVER]
			#server settings
			"host":				"2a00:7b80:3019:12::84e6:a83", 
			"port":				6667, 
		
			#[BOT DETAILS]
			#Set bot details, chans etc..
			"nick":				"pyTsunku", 
			"altnick": 			"pyTunkio", 
			"realname":			"pyTsunku", 
			"ident":			"pyTsunku", 
			"version":			"pyBot version 0.2.2", 
			"chans":			"#tsunku",

			#[OPERS]
			#Bot operators
			"opers":			"hrna@oper.aquanet.fi,jaska@127.0.0.1",

			#[MODULES]
			#Modules & System modules, you better not touch system modules
			"sysmodules":			"logger_daemon,title", #Do not touch this line!!
			"modules":			"cmd,clock,op,version,fmi,currency",

			#[LOGGING DAEMON]
			#Loggin
			"logging":			"true",
			"timeformat":			"%H:%M:%S", #Will be shown in the log as [13:31:27]
			"TimestampBrackets":		"[,]",

			#[DEV DEBUGGING]
			#Bot debugging true/false
			"debug":			"true"
				
		  }
			#Everything is editable, but if you dont know what you're doing, dont touch anything else than bot details.
