import subprocess
import platform
import re
import sysErrorLog

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
			total_mem = round(int(string[2])/1024/1024)
			process2 = subprocess.Popen(["top -l 1 | grep PhysMem: | awk '{print $6}'"], stdout=PIPE, stderr=PIPE, shell=True)
			free_mem, stderroutput = process2.communicate()
			free_mem = free_mem.decode("utf-8").strip()
			free_mem = total_mem - int(free_mem[:-1])
			
			## Uptime
			process3 = subprocess.Popen(["uptime"], stdout=PIPE, stderr=PIPE)
			uptime, stderroutput = process3.communicate()
			uptime = uptime.decode("utf-8").strip()
			uptime = re.search("( )\d(.*?),(.*?),", uptime).group(1).rstrip(",").strip()

			## GPU
			process4 = subprocess.Popen(['system_profiler', 'SPDisplaysDataType'], stdout=PIPE, stderr=PIPE)
			gpu, stderroutput = process4.communicate()
			gpu = gpu.decode("utf-8").strip()
			vram = re.search("VRAM \(Total\):+(.*)", gpu).group(1).strip()
			gpu = re.search("Chipset Model:+(.*)", gpu).group(1).strip()
						
			self.send_chan("I'm running on OS X {0} {1} with Python {2} <> CPU: {3} <> GPU: {4} {5} <> Uptime: {6} <> Mem Usage: {7}/{8} MiB"
				.format(platform.mac_ver()[0], platform.platform(), 
					platform.python_version()," ".join(string[1][:-11].split()), gpu, vram, uptime, free_mem, total_mem))		
		elif "Linux" in platform.system():
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
			uptime = uptime.decode("utf-8").strip()
			uptime = re.search("( )\d(.*?),(.*?),", uptime.strip()).group(0).rstrip(",").strip()

			self.send_chan("I'm running on {0} with Python {1} <> CPU: {2} <> Uptime: {3} <> Mem Usage: {4}/{5} MiB"
				.format(platform.platform(), 
					platform.python_version(), " ".join(cpu.split()), uptime, used_mem, total_mem))
		else:
			self.send_chan("Your operating system isn't supported :(")
				
	except Exception as e:
		self.errormsg = "[ERROR]-[sysinfo] sysinfo() stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
