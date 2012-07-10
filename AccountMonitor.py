import Config, socket, re, time
from PyQt4 import QtCore, QtGui
from sourcelib import SourceQuery

import Sandboxie

class AccountManager():
	def __init__(self, window):
		self.settings = Config.settings
		self.window = window
		self.usedPorts = []
		self.createdSandboxes = []
		self.sandboxieINIIsModified = False

	def startAccounts(self, action, accounts):
		easy_sandbox_mode = self.settings.get_option('Settings', 'easy_sandbox_mode')
		self.commands = []

		# Error dialogs if no accounts selected
		if len(accounts) == 0:
			if action == 'idle':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to idle')
			elif action == 'idle_unsandboxed':
				QtGui.QMessageBox.information(self.window, 'No account selected', 'Please select an account to idle')
			elif action == 'start_steam':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to start Steam with')
			elif action == 'start_TF2':
				QtGui.QMessageBox.information(self.window, 'No accounts selected', 'Please select at least one account to start TF2 with')

		# Error dialog if > 1 accounts selected and trying to run them all unsandboxed
		elif action == 'idle_unsandboxed' and len(accounts) > 1:
			QtGui.QMessageBox.information(self.window, 'Too many accounts selected', 'Please select one account to idle')
		# Error dialog if easy sandbox mode is on and program isn't run with elevated privileges
		elif easy_sandbox_mode == 'yes' and action != 'idle_unsandboxed' and not self.window.runAsAdmin():
			QtGui.QMessageBox.information(self.window, 'Easy sandbox mode requires admin', 'TF2Idle requires admin privileges to create/modify sandboxes. Please run the program as admin.')
		else:
			steamlocation = self.settings.get_option('Settings', 'steam_location')
			secondary_steamapps_location = self.settings.get_option('Settings', 'secondary_steamapps_location')
			sandboxielocation = self.settings.get_option('Settings', 'sandboxie_location')

			for account in accounts:
				username = self.settings.get_option('Account-' + account, 'steam_username')
				password = self.settings.get_option('Account-' + account, 'steam_password')
				sandboxname = self.settings.get_option('Account-' + account, 'sandbox_name')
				if self.settings.get_option('Account-' + account, 'sandbox_install') == '' and easy_sandbox_mode == 'yes':
					sandbox_install = secondary_steamapps_location
				else:
					sandbox_install = self.settings.get_option('Account-' + account, 'sandbox_install')
				# Check if account has launch parameters that override main parameters
				if self.settings.has_option('Account-' + account, 'launch_options') and self.settings.get_option('Account-' + account, 'launch_options') != '':
					steamlaunchcommand = self.settings.get_option('Account-' + account, 'launch_options')
				else:
					steamlaunchcommand = self.settings.get_option('Settings', 'launch_options')

				if not self.sandboxieINIIsModified and easy_sandbox_mode == 'yes':
					Sandboxie.backupSandboxieINI()
					self.mainwindow.sandboxieINIHasBeenModified()

				if action == 'idle_unsandboxed':
					portpresent, portnumber = self.returnServerPort(steamlaunchcommand)
					if not portpresent:
						steamlaunchcommand += ' +hostport {0}'.format(str(portnumber))
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (steamlocation, username, password, steamlaunchcommand)

				else:
					if action == 'idle':
						portpresent, portnumber = self.returnServerPort(steamlaunchcommand)
						if not portpresent:
							steamlaunchcommand += ' +hostport {0}'.format(str(portnumber))
						command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (sandbox_install, username, password, steamlaunchcommand)
					elif action == 'start_steam':
						command = r'"%s/Steam.exe" -login %s %s' % (sandbox_install, username, password)
					elif action == 'start_TF2':
						command = r'"%s/Steam.exe" -login %s %s -applaunch 440' % (sandbox_install, username, password)

					if easy_sandbox_mode == 'yes' and self.settings.get_option('Account-' + account, 'sandbox_install') == '':
						self.commandthread.addSandbox('TF2Idle' + username)
						self.createdSandboxes.append(username)
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, 'TF2Idle' + username, command)
					else:
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)

				self.commands.append(command)
			self.commandthread = Sandboxie.SandboxieThread()
			self.commandthread.addCommands(self.commands)
			self.commandthread.start()

	def returnServerPort(self, launcharguments):
		portnumberRE = re.compile(r'\+hostport\s(\d+)')
		res = portnumberRE.search(launcharguments)
		if res:
			portnumber = int(res.group(1))
			self.usedPorts.append(portnumber)
			return True, portnumber
		else:
			portnumber = 27015
			while True:
				if portnumber in self.usedPorts:
					portnumber += 1
					continue
				else:
					# Check if port is in use by another client started outside of TF2Idle
					if self.returnServerPlayers(portnumber) is None:
						self.usedPorts.append(portnumber)
						return False, portnumber
					else:
						self.usedPorts.append(portnumber)
						portnumber += 1
						continue

	def returnServerPlayers(self, port):
		address = socket.gethostbyname(socket.gethostname())
		try:
			players = []
			server = SourceQuery.SourceQuery(address, port, 3.0)
			for player in server.player():
				players.append(player['name'])
			return players
		except:
			# Server ded
			return None

class AccountHealthMonitorThread(QtCore.QThread):
	def __init__(self, manager, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.manager = manager
		self.accounts = []
		self.alive = True

	def addAccount(self, account):
		self.accounts.append(account)

	def removeAccount(self, account):
		self.accounts.remove(account)

	def kill(self):
		self.alive = False

	def run(self):
		while self.alive:
			for account in self.accounts:
				serverplayers = self.manager.returnServerPlayers(account['port'])
				if serverplayers is None or len(serverplayers) == 0:
					#ded
					#alert manager to reconnect
			time.sleep(15*60)

class SmartIdleThread(QtCore.QThread):
	def __init__(self, maxaccounts, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.activeaccounts = []
		self.queuedaccounts = []
		self.maxaccounts = maxaccounts