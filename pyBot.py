#!/usr/bin/env python3
## Import needed modules

import time

from threading import Thread
from pyBotCore import pyBot, Flood


## Run the bot and flood counter in own threads
def initialize():
	bot = Thread(target=pyBot)
	fld = Thread(target=Flood)

	bot.daemon = True
	bot.start()
	fld.daemon = True
	fld.start()
	while True: ## Keep the main thread alive
		time.sleep(1)
try:
	initialize()
except Exception:
	""" 
	Logging this kind of error at this point is not possible, i have no idea how would i deal this right now..
	#errormsg = "[ERROR]-[Core] Connection failure, attempting to reconnect"
	#sys_error_log.log( self ) ## LOG the error 
	"""

	## time sleep 10 because we dont want to reconnect too fast if something goes wrong.
	time.sleep(10)
	initialize()	
except KeyboardInterrupt:
	#os._exit(1)
	print( "Ctrl+C, Quitting!" )
