import time

def clock( self ):
		self.send_chan( self.get_nick() + ", The time is " + time.strftime( "%X" ))