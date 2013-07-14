## Klo
import time

def klo( self ):
		self.send_chan( self.get_nick() + ", kello on " + self.msg[2] + time.strftime( "%X" ))
