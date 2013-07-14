## Klo
import time

def klo( self ):
		self.send_chan( self.get_nick() + ", The time is " + time.strftime( "%X" ))
