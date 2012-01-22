import Config, subprocess, shutil, os, codecs
from PyQt4 import QtCore, QtGui

sandboxfile = r'C:\Windows\Sandboxie.ini'
backupfile = r'C:\Windows\Sandboxie_backup.ini'

class SandboxieThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.createdSandboxes = []

	def addSandbox(self, sandboxname):
		if sandboxname in self.createdSandboxes:
			pass
		else:
			secondary_steamapps_location = self.settings.get_option('Settings', 'secondary_steamapps_location')
			sandboxielocation = self.settings.get_option('Settings', 'sandboxie_location')

			config = codecs.open(sandboxfile, 'rb', 'UTF-16LE').read()
			
			sandboxstring = u"""\r\n[%s]\r\n""" % sandboxname
			sandboxstring += u"""\r\nEnabled=y"""
			sandboxstring += u"""\r\nConfigLevel=6"""
			sandboxstring += u"""\r\nAutoRecover=y"""
			sandboxstring += u"""\r\nAutoDelete=yes"""
			sandboxstring += u"""\r\nTemplate=LingerPrograms"""
			sandboxstring += u"""\r\nTemplate=AutoRecoverIgnore"""
			sandboxstring += u"""\r\nRecoverFolder=%Personal%"""
			sandboxstring += u"""\r\nRecoverFolder=%Favorites%"""
			sandboxstring += u"""\r\nRecoverFolder=%Desktop%"""
			sandboxstring += u"""\r\nOpenFilePath=%s""" % secondary_steamapps_location + os.sep
			sandboxstring += u"""\r\nOpenFilePath=%s""" % secondary_steamapps_location + os.sep + 'Steam.exe'
			
			f = codecs.open(sandboxfile, 'wb', 'UTF-16LE')
			f.write(config + sandboxstring)
			f.close()
			self.createdSandboxes.append(sandboxname)

			response = subprocess.call([sandboxielocation + os.sep + 'start.exe', '/reload'])
	
	def runCommand(self, command):
		returnCode = subprocess.call(command)

def backupSandboxieINI():
	shutil.copy(sandboxfile, backupfile)

def restoreSandboxieINI():
	shutil.copy(backupfile, sandboxfile)