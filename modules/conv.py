import sys_error_log

def conv ( self ):

	if len(self.msg) < 6:
		self.send_chan("Usage: !conv <amount> <from> <to>")
	if len(self.msg) == 6:
		try:
			amount = float(self.msg[4])
		except ValueError:
			amount = 1.00
		frm = self.msg[5].strip()
		#to = self.msg[6].strip()
		output = ""

		try:
			if frm == "mm":
				result = round(amount * 0.03937, 5)
				output = "{0} millimeters is {1} inches".format(amount, result)
			elif frm == "in":
				result = round(amount * 2.54, 2)
				if result < 100:
					output = output = "{0} inches is {1} centimeters".format(amount, result)
				else:
					result = result/100
					output = output = "{0} inches is {1} meters".format(amount, result)
			elif frm == "cm":
				result = round(amount * 0.3937, 2)
				output = "{0} centimeters is {1} inches".format(amount, result)
			elif frm == "m":
				result = round(amount * 1.0936, 2)
				output = "{0} meters is {1} yards".format(amount, result)
			elif frm == "yd":
				result = round(amount * 0.9144, 2)
				if result < 1000:
					output = "{0} yards is {1} meters".format(amount, result)
				else:
					result = result / 1000
					output = "{0} yards is {1} kilometers".format(amount, result)
			elif frm == "km":
				result = round(amount * 0.6214, 2)
				output = "{0} kilometers is {1} miles".format(amount, result)
			elif frm == "miles":
				result = round(amount * 1.6093, 2)
				if result < 1:
					result = result*1000
					output = "{0} miles is {1} meters".format(amount, result)
				else:
					output = "{0} miles is {1} kilometers".format(amount, result)
			else:
				output = "I don't know how to convert {0} {1}(s) :(".format(amount, frm)

			self.send_chan(output)

		except Exception as e:
			self.errormsg = "[ERROR]-[Conv] stating: {0}".format(e)
			sys_error_log.log( self ) ## LOG the error
			if self.config["debug"] == "true":
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	else:
		self.send_chan("Usage: !conv <amount> <from> <to>")
