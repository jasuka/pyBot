import re

def modecheck (self):
	file = "modules/data/automodes.txt"
	with open(file, "r", encoding="UTF-8") as modes:
		for line in modes:
			if re.search("\\b"+self.get_nick()+":\\b", line, flags=re.IGNORECASE):
				spl = line.split(":")
				print(spl[0]+" "+spl[1])
				if spl[1].strip() == "ao":
					self.send_data("MODE {0} +o {1}".format(self.msg[2][1:].strip(),self.get_nick()))
