import sys_error_log

def conv ( self ):

	if len(self.msg) < 7:
		self.send_chan("Usage: !conv <amount> <from> <to>")
	if len(self.msg) == 7:
		try:
			amount = float(self.msg[4])
		except ValueError:
			amount = 1.00
		frm = self.msg[5].strip()
		to = self.msg[6].strip()
		output = ""

		try:
			if "mm" in frm and "in" in to:
				output = "{0} millimeters is {1} inches".format(amount, amount * 0.03937)
			elif "in" in frm and "mm" in to:
				output = "{0} inches is {1} millimeters".format(amount, amount * 2540)
			elif "cm" in frm and "in" in to:
				output = "{0} centimeters is {1} inches".format(amount, amount * 0.3937)
			elif "in" in frm and "cm" in to:
				output = "{0} inches is {1} centimeters".format(amount, amount * 2.54)
			else:
				output = "I don't know how to convert {0} {1}(s) to {2} :(".format(amount, frm, to)

			self.send_chan(output)
		except Exception as e:
			self.errormsg = "[ERROR]-[Conv] stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
