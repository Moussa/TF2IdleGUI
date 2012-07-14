import Config, subprocess, shutil, os, codecs
from PyQt4 import QtCore, QtGui

sandboxfile = os.environ['WINDIR'] + os.sep + 'Sandboxie.ini'
backupfile = os.environ['WINDIR'] + os.sep + 'Sandboxie_backup.ini'

class SandboxieManager():
	def __init__(self):
		self.settings = Config.settings
		self.createdSandboxes = []

	def addSandbox(self, sandboxname):
		if sandboxname in self.createdSandboxes:
			pass
		else:
			steam_location = self.settings.get_option('Settings', 'steam_location')
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
			sandboxstring += u"""\r\nOpenFilePath=%s""" % steam_location + os.sep
			sandboxstring += u"""\r\nOpenFilePath=%s""" % steam_location + os.sep + 'Steam.exe'

			f = codecs.open(sandboxfile, 'wb', 'UTF-16LE')
			f.write(config + sandboxstring)
			f.close()
			self.createdSandboxes.append(sandboxname)

			subprocess.call([sandboxielocation + os.sep + 'start.exe', '/reload'])

def backupSandboxieINI():
	shutil.copy(sandboxfile, backupfile)

def restoreSandboxieINI():
	shutil.copy(backupfile, sandboxfile)