import subprocess
import re
import sysErrorLog
import syscmd

def git(self):

	if self.get_host() not in self.config["opers"]:
		self.errormsg = "[NOTICE]-[git] Unauthorized git reguest from {0}".format(self.get_host())
		sysErrorLog.log( self )
		return
	try:
		PIPE = subprocess.PIPE
		process = subprocess.Popen(['git', 'pull'], stdout=PIPE, stderr=PIPE)
		stdoutput, stderroutput = process.communicate()
	
		if self.config["debug"]:
			output = stdoutput.decode("utf-8")
			output += stderroutput.decode("utf-8")
			print(output)
			self.send_pm(output)
			
		if "fatal" in stdoutput.decode("utf-8"):
			self.send_chan("Git pull failed!")
		elif "Already up-to-date." in stdoutput.decode("utf-8"):
			self.send_chan("Already up-to-date!")
			self.activitymsg = "git: Already up-to-date!"
			sysErrorLog.activity ( self )
			syscmd.fileLatestCommit(self,syscmd.getCommits(self))
		elif "overwritten by merge" in stderroutput.decode("utf-8"):
			self.send_chan("There was a conflict during merge! Please solve manually!")
		elif "pyBot.py" in stdoutput.decode("utf-8"):
			self.send_chan("Pull succeeded, core updated, restarting!")
			self.activitymsg = "git: Pull succeeded, core updated!"
			sysErrorLog.activity ( self )
			syscmd.fileLatestCommit(self,syscmd.getCommits(self))
			self.restart()
		elif "pyBotCore.py" in stdoutput.decode("utf-8"):
			self.send_chan("Pull succeeded, core updated, restarting!")
			self.activitymsg = "git: Pull succeeded, core updated!"
			sysErrorLog.activity ( self )
			syscmd.fileLatestCommit(self,syscmd.getCommits(self))
			self.restart()
		elif "create mode" in stdoutput.decode("utf-8"):
			mods = re.findall(r"\create mode 100644 modules/(.*.py)", stdoutput.decode("utf-8"))
			modules = ""
			for x in mods:
				modules += "{0} ".format(x[:-3])
				self.load(x[:-3])
				syscmd.fileLatestCommit(self,syscmd.getCommits(self))
		else:
			self.send_chan("Pull succeeded, remember to reload the modules!")
			self.activitymsg = "git: Pull succeeded!"
			sysErrorLog.activity ( self )
			syscmd.fileLatestCommit(self,syscmd.getCommits(self))
	
	except Exception as e:
		self.errormsg = "[ERROR]-[git] git() stating: {0}".format(e)
		sysErrorLog.log( self ) ## LOG the error
		if self.config["debug"]:
			print("{0}{1}{2}".format(self.color("red"), self.errormsg, self.color("end")))
