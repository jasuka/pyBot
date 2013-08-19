import subprocess
import platform

def sysinfo(self):


	try:
		PIPE = subprocess.PIPE

		if "Darwin" in platform.system():

			## CPU and Total RAM
			process = subprocess.Popen(['sysctl', 'machdep.cpu.brand_string', 'hw.memsize'], stdout=PIPE, stderr=PIPE)
			cpu, stderroutput = process.communicate()
		
			## Used MEM
			process2 = subprocess.Popen(["top -l 1 | grep PhysMem: | awk '{print $2}'"], stdout=PIPE, stderr=PIPE, shell=True)
			used_mem, stderroutput = process2.communicate()
			used_mem = used_mem.decode("utf-8").strip()
			used_mem = used_mem[:-1]
			string = cpu.decode("utf-8")
			string = string.split(":")
			total_mem = round(int(string[2])/1024/1024)
			
			## Uptime
			process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
			uptime, stderroutput = process3.communicate()
			uptime = uptime.decode("utf-8").strip()
			temp = uptime.split(" ")
			uptime = "{0} {1} {2}".format(temp[3], temp[4], temp[6][:-1])

			self.send_chan("OS: {0} <> Python: {1} <> CPU: {2} <> Uptime: {3} <> Mem Usage: {4}/{5} MiB".format(platform.platform(), 
					platform.python_version(), " ".join(string[1][:-11].split()), uptime, used_mem, total_mem))			
			
		if "Linux" in platform.system():
			process2 = subprocess.Popen(["top -n 1 | grep 'KiB Mem:' | awk '{print $4 " " $6}'"], stdout=PIPE, stderr=PIPE, shell=True)
			mem, stderroutput = process2.communicate()
			mem = mem.decode("utf-8").strip()
			mem = mem.split(" ")
			used_mem = int(mem[1])/1024
			total_mem = int(mem[0])/1024

			## Uptime
			process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
			uptime, stderroutput = process3.communicate()
			uptime = uptime.decode("utf-8").strip()
			temp = uptime.split(" ")
			uptime = "{0} {1} {2}".format(temp[3], temp[4], temp[6][:-1])

			self.send_chan("OS: {0} <> Python: {1} <> Uptime: {2} <> Mem Usage: {3}/{4} MiB".format(platform.platform(), 
					platform.python_version(), uptime, used_mem, total_mem))	
				
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)