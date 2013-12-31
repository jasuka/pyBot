import subprocess
import platform

def sysinfo(self):


	try:
		if "Darwin" in platform.system():
			PIPE = subprocess.PIPE
			## CPU and Total RAM
			process = subprocess.Popen(['sysctl', 'machdep.cpu.brand_string', 'hw.memsize'], stdout=PIPE, stderr=PIPE)
			cpu, stderroutput = process.communicate()
			string = cpu.decode("utf-8")
			string = string.split(":")
		
			## Used MEM
			process2 = subprocess.Popen(["top -l 1 | grep PhysMem: | awk '{print $2}'"], stdout=PIPE, stderr=PIPE, shell=True)
			used_mem, stderroutput = process2.communicate()
			used_mem = used_mem.decode("utf-8").strip()
			used_mem = used_mem[:-1]
			total_mem = round(int(string[2])/1024/1024)
			
			## Uptime
			process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
			uptime, stderroutput = process3.communicate()
			uptime = uptime.decode("utf-8").strip()
			temp = uptime.split(" ")
			uptime = "{0} {1} {2}".format(temp[3], temp[4], temp[5][:-1])

			self.send_chan("I'm running on OS X {0} {1} with Python {2} <> CPU: {3} <> Uptime: {4} <> Mem Usage: {5}/{6} MiB".format(platform.mac_ver()[0], platform.platform(), 
							platform.python_version()," ".join(string[1][:-11].split()), uptime, used_mem, total_mem))		
			
		if "Linux" in platform.system():
			PIPE = subprocess.PIPE
			
			## CPU and Total RAM
			process = subprocess.Popen(['cat /proc/cpuinfo | grep "model name" | head -n1'], stdout=PIPE, stderr=PIPE, shell=True)
			cpu, stderroutput = process.communicate()
			cpu = cpu.decode("utf-8").strip()
			cpu = cpu.split(":")
			cpu = cpu[1]
			
			## MEM // Have to use free -m....
			process2 = subprocess.Popen(["free -m | grep Mem | awk '{print $2 \" \" $3}'"], stdout=PIPE, stderr=PIPE, shell=True)
			mem, stderroutput = process2.communicate()
			mem = mem.decode("utf-8").strip()
			mem = mem.split(" ")
			used_mem = mem[1]
			total_mem = mem[0]

			## Uptime
			process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
			uptime, stderroutput = process3.communicate()
			uptime = uptime.decode("utf-8")
			temp = " ".join(uptime.split()).split(" ")
			uptime = "{0} {1} {2}".format(temp[2], temp[3], temp[4][:-1])

			self.send_chan("I'm running on {0} with Python {1} <> CPU: {2} <> Uptime: {3} <> Mem Usage: {4}/{5} MiB".format(platform.platform(), 
					platform.python_version(), " ".join(cpu.split()), uptime, used_mem, total_mem))	
				
	except Exception as e:
		if self.config["debug"] == "true":
			print("Error occured in sysinfo module: "+e)
