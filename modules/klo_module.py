## Klo
import time

def klo( self, data ):
		self.send_chan( self.get_nick() + ", kello on " + time.strftime( "%X" ))
