import syscmd
def version (self):
	self.send_chan("{0} (Build: {1}) https://github.com/jasuka/pyBot/releases".format(self.version,syscmd.readRevisionNumber(self)))
