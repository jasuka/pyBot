import subprocess

def git(self):

	if self.get_host() not in self.config["opers"]:
		return
	try:
		PIPE = subprocess.PIPE
		process = subprocess.Popen(['git', 'pull'], stdout=PIPE, stderr=PIPE)
		stdoutput, stderroutput = process.communicate()
	
		if self.config["debug"] == "true":
			print(stdoutput.decode("utf-8"))
			
		if "fatal" in stdoutput.decode("utf-8"):
			self.send_chan("Git pull failed!")
		if "Already up-to-date." in stdoutput.decode("utf-8"):
			self.send_chan("Already up-to-date!")
		if "pyBot.py" in stdoutput.decode("utf-8"):
			self.send_chan("Pull succeeded, core updated, restarting!")
			self.restart()
		if "Already up-to-date." not in stdoutput.decode("utf-8"):
			self.send_chan("Pull succeeded, remember to reload the modules")
	
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)