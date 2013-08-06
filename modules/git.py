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
			self.send_notice("Git pull failed")
		if "pyBot.py" in stdoutput.decode("utf-8"):
			self.send_notice("Pull succeeded, core updated, restarting!")
			self.restart()
		else:
			self.send_notice("Pull succeeded, remember to reload the modules")
	
	except Exception as e:
		if self.config["debug"] == "true":
			print(e)