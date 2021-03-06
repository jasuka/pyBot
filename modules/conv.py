import re
import sysErrorLog

def conv ( self ):

	if len(self.msg) == 5 and self.msg[4].strip() == "units":
		self.send_chan("I know: km, m, cm, mm, l, ml, ft, yd, miles, floz, gal, kg, g, lb, oz, c, f, k")
		return
	if len(self.msg) < 6:
		self.send_chan("Usage: !conv <amount> <unit> || !conv units")
		return
	if len(self.msg) == 6:
		try:
			amount = float(re.sub(",", ".", self.msg[4]))
		except ValueError:
			amount = 1.00
		frm = self.msg[5].strip()
		output = ""

		try:
			## Length conversions
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
			elif frm == "ft":
				result = round(amount * 30.48, 2)
				if result > 100:
					result = round(result / 100, 2)
					output = "{0} feet is {1} meters".format(amount, result)
				else:
					output = "{0} feet is {1} centimeters".format(amount, result)
			## Volume conversions
			elif frm == "floz":
				result = round(amount * 29.574, 3)
				if result < 1000:
					output = "{0} fluid ounces is {1} milliliters".format(amount, result)
				else:
					result = round(result / 1000, 2)
					output = "{0} fluid ounces is {1} liters".format(amount, result)
			elif frm == "ml":
				result = round(amount / 29.574, 3)
				output = "{0} milliliters is {1} fluid ounces".format(amount, result)
			elif frm == "gal":
				result = round(amount * 3.7854, 4)
				output = "{0} gallons is {1} liters".format(amount, result)
			elif frm == "l":
				result = round(amount / 3.7854, 4)
				output = "{0} liters is {1} gallons".format(amount, result)
			## Mass conversions
			elif frm == "g":
				result = round(amount * 0.0353, 4)
				output = "{0} g is {1} ounces".format(amount, result)
			elif frm == "oz":
				result = round(amount * 28.35, 2)
				if result < 1000:
					output = "{0} ounces is {1} grams".format(amount, result)
				else:
					result = round(result / 1000, 2)
					output = "{0} ounces is {1} kilograms".format(amount, result)
			elif frm == "kg":
				result = round(amount * 2.2046, 4)
				output = "{0} kilograms is {1} pounds".format(amount, result)
			elif frm == "lb":
				result = round(amount * 0.4536, 4)
				if result < 1:
					result = round(result * 1000, 2)
					output = "{0} pounds is {1} grams".format(amount, result)
				else:
					result = round(result, 2)
					output = "{0} pounds is {1} kilograms".format(amount, result)
			## Temperature conversions
			elif frm == "c":
				fahrenheit = round(amount * 1.8 + 32, 2)
				kelvin = round(amount + 273.15, 2)
				output = "{0} °C is {1} °F ({2} K)".format(amount, fahrenheit, kelvin)
			elif frm == "f":
				celsius = round((amount - 32) / 1.8, 2)
				output = "{0} °F is {1} °C".format(amount, celsius)
			elif frm == "k":
				celsius = round(amount - 273.15, 2)
				output = "{0} K is {1} °C".format(amount, celsius)
			else:
				output = "I don't know how to convert {0} {1}(s) :(".format(amount, frm)

			self.send_chan(output)

		except Exception as e:
			self.errormsg = "[ERROR]-[Conv] stating: {0}".format(e)
			sysErrorLog.log( self ) ## LOG the error
			if self.config["debug"]:
				print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
	else:
		self.send_chan("Usage: !conv <amount> <unit> || !conv units")
