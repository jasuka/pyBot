import subprocess
import platform

def sysinfo(self):

	try:
		PIPE = subprocess.PIPE

		## CPU and Total RAM
		process = subprocess.Popen(['sysctl', 'machdep.cpu.brand_string', 'hw.memsize'], stdout=PIPE, stderr=PIPE)
		cpu, stderroutput = process.communicate()

		## Used MEM
		process2 = subprocess.Popen(["top -l 1 | grep PhysMem: | awk '{print $2}'"], stdout=PIPE, stderr=PIPE, shell=True)
		used_mem, stderroutput = process2.communicate()
		used_mem = used_mem.decode("utf-8").strip()
		used_mem = used_mem[:-1]

		## Linux top -n 1 | grep "KiB Mem:" | awk '{print $4}' and top -n 1 | grep "KiB Mem:" | awk '{print $6}'

		## Uptime
		process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
		uptime, stderroutput = process3.communicate()
		uptime = uptime.decode("utf-8").strip()
		temp = uptime.split(" ")
		uptime = "{0} {1} {2}".format(temp[3], temp[4], temp[6][:-1])

		string = cpu.decode("utf-8")
		string = string.split(":")
		mem = round(int(string[2])/1024/1024)


		self.send_chan("OS: {0} <> Python: {1} <> CPU: {2} <> Uptime: {3} <> Mem Usage: {4}/{5} MiB".format(platform.platform(), 
				platform.python_version(), " ".join(string[1][:-11].split()), uptime, used_mem, mem))
				
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)