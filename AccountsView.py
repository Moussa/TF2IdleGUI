import Config, subprocess, webbrowser, shutil, os, ctypes
import Sandboxie
from PyQt4 import QtCore, QtGui
from sets import Set
from AccountDialog import Ui_AccountDialog
from GroupsDialog import Ui_GroupsDialog

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

class Worker(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)

	def run(self):
		self.settings = Config.settings
		self.settings.set_section('Settings')
		steam_location = self.settings.get_option('steam_location')
		secondary_steamapps_location = self.settings.get_option('secondary_steamapps_location')
		gcfs = ['team fortress 2 content.gcf','team fortress 2 materials.gcf','team fortress 2 client content.gcf']

		if not os.path.exists(steam_location + os.sep + 'steamapps' + os.sep):
			self.returnMessage('Path does not exist', 'The Steam folder path does not exist. Please check settings')
		elif not os.path.exists(secondary_steamapps_location):
			self.returnMessage('Path does not exist', 'The secondary Steam folder path does not exist. Please check settings')
		else:
			self.returnMessage('Info', 'Remember to start the backup Steam installation unsandboxed to finish the updating process')
			self.emit(QtCore.SIGNAL('StartedCopyingGCFs'))
			try:
				for file in gcfs:
					shutil.copy(steam_location + os.sep + 'steamapps' + os.sep + file, secondary_steamapps_location)
			except:
				self.returnMessage('File copy error', 'The GCFs could not be copied')
			self.emit(QtCore.SIGNAL('FinishedCopyingGCFs'))
		
	def returnMessage(self, title, message):
		self.emit(QtCore.SIGNAL('returnMessage'), title, message)

class curry(object):
	def __init__(self, func, *args, **kwargs):
		self._func = func
		self._pending = args[:]
		self._kwargs = kwargs
	def __call__(self, *args, **kwargs):
		if kwargs and self._kwargs:
			kw = self._kwargs.copy()
			kw.update(kwargs)
		else:
			kw = kwargs or self._kwargs
		return self._func(*(self._pending + args), **kw)

class AccountsView(QtGui.QWidget):
	def __init__(self, mainwindow):
		QtGui.QWidget.__init__(self)
		self.mainwindow = mainwindow
		self.settings = Config.settings
		self.toolBars = []
		self.accountButtons = []
		self.chosenGroupAccounts = []
		self.createdSandboxes = []
		self.sandboxieINIIsModified = False
		self.commandthread = Sandboxie.SandboxieThread()

		self.updateWindow(construct = True)

	def updateWindow(self, construct=False, disableUpdateGCFs=False):
		
		# Add vertical toolbar actions	

		addAccountIcon = QtGui.QIcon()
		addAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/add_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.addAccountAction = self.mainwindow.vtoolBar.addAction(addAccountIcon, 'Add account')
		QtCore.QObject.connect(self.addAccountAction, QtCore.SIGNAL('triggered()'), self.openAccountDialog)
		
		editAccountIcon = QtGui.QIcon()
		editAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/edit_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.editAccountAction = self.mainwindow.vtoolBar.addAction(editAccountIcon, 'Edit account')
		QtCore.QObject.connect(self.editAccountAction, QtCore.SIGNAL('triggered()'), curry(self.openAccountDialog, editAccount=True))
		
		removeAccountIcon = QtGui.QIcon()
		removeAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/remove_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.deleteAccountsAction = self.mainwindow.vtoolBar.addAction(removeAccountIcon, 'Delete account')
		QtCore.QObject.connect(self.deleteAccountsAction, QtCore.SIGNAL('triggered()'), self.deleteAccounts)
		
		selectGroupIcon = QtGui.QIcon()
		selectGroupIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/select_group.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.selectGroupsAction = self.mainwindow.vtoolBar.addAction(selectGroupIcon, 'Select Groups')
		QtCore.QObject.connect(self.selectGroupsAction, QtCore.SIGNAL('triggered()'), self.selectGroups)
		
		viewBackpackIcon = QtGui.QIcon()
		viewBackpackIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/backpack.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.viewBackpackAction = self.mainwindow.vtoolBar.addAction(viewBackpackIcon, 'View backpack')
		QtCore.QObject.connect(self.viewBackpackAction, QtCore.SIGNAL('triggered()'), self.openBackpack)
		
		# Add horizontal toolbar actions
		switchToLogViewIcon = QtGui.QIcon()
		switchToLogViewIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_log.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.switchToLogViewAction = self.mainwindow.htoolBar.addAction(switchToLogViewIcon, 'Drop log view')
		QtCore.QObject.connect(self.switchToLogViewAction, QtCore.SIGNAL('triggered()'), self.changeMainWindowView)
		
		self.mainwindow.htoolBar.addSeparator()
		
		startIdleIcon = QtGui.QIcon()
		startIdleIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_idle.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startIdleAction = self.mainwindow.htoolBar.addAction(startIdleIcon, 'Start idling')
		QtCore.QObject.connect(self.startIdleAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='idle'))
		
		startIdleUnsandboxedIcon = QtGui.QIcon()
		startIdleUnsandboxedIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_idle_unsandboxed.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startIdleUnsandboxedAction = self.mainwindow.htoolBar.addAction(startIdleUnsandboxedIcon, 'Start idling (no sandbox)')
		QtCore.QObject.connect(self.startIdleUnsandboxedAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='idle_unsandboxed'))
		
		startTF2Icon = QtGui.QIcon()
		startTF2Icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_tf2.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startTF2Action = self.mainwindow.htoolBar.addAction(startTF2Icon, 'Start TF2')
		QtCore.QObject.connect(self.startTF2Action, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='start_TF2'))
		
		startSteamIcon = QtGui.QIcon()
		startSteamIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_steam.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startSteamAction = self.mainwindow.htoolBar.addAction(startSteamIcon, 'Start Steam')
		QtCore.QObject.connect(self.startSteamAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='start_steam'))
		
		self.mainwindow.htoolBar.addSeparator()
		
		updateGCFsIcon = QtGui.QIcon()
		if not disableUpdateGCFs:
			updateGCFsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/update_gcfs.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.updateGCFsAction = self.mainwindow.htoolBar.addAction(updateGCFsIcon, 'Update GCFs')
			QtCore.QObject.connect(self.updateGCFsAction, QtCore.SIGNAL('triggered()'), self.updateGCFs)
		else:
			updateGCFsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/updating_gcfs.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.updateGCFsAction = self.mainwindow.htoolBar.addAction(updateGCFsIcon, 'Updating GCFs')
		
		terminateSandboxIcon = QtGui.QIcon()
		terminateSandboxIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/terminate_sandbox.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.terminateSandboxAction = self.mainwindow.htoolBar.addAction(terminateSandboxIcon, 'Terminate sandbox')
		QtCore.QObject.connect(self.terminateSandboxAction, QtCore.SIGNAL('triggered()'), curry(self.modifySandboxes, action='/terminate'))
		
		emptySandboxIcon = QtGui.QIcon()
		emptySandboxIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/delete_sandbox.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.emptySandboxAction = self.mainwindow.htoolBar.addAction(emptySandboxIcon, 'Empty sandbox')
		QtCore.QObject.connect(self.emptySandboxAction, QtCore.SIGNAL('triggered()'), curry(self.modifySandboxes, action='delete_sandbox'))

		if construct:
			self.gridLayout = QtGui.QGridLayout(self)
			self.gridLayout.setMargin(0)
			
			self.verticalLayout = QtGui.QVBoxLayout()
			self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
			
			# Add keyboard shortcut to select all account boxes
			QtGui.QShortcut(QtGui.QKeySequence('Ctrl+A'), self.mainwindow, self.SelectAllAccounts)

			QtCore.QMetaObject.connectSlotsByName(self)

		self.updateAccountBoxes()

	def changeMainWindowView(self):
		self.mainwindow.changeView('log')

	def updateAccountBoxes(self):
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.text()))
			widget.close()
			del widget

		self.accountButtons = []
		row = 0
		column = 0
		self.settings.set_section('Settings')
		numperrow = int(self.settings.get_option('ui_no_of_columns'))
		ui_account_box_font_size = self.settings.get_option('ui_account_box_font_size')
		ui_account_box_icon_size = int(self.settings.get_option('ui_account_box_icon_size'))
		ui_account_box_icon = self.settings.get_option('ui_account_box_icon')

		# Sort account boxes alphabetically
		sortedlist = []
		for account in list(Set(self.settings.get_sections()) - Set(['Settings'])):
			self.settings.set_section(account)
			if self.settings.get_option('account_nickname') != '':
				sortedlist.append((self.settings.get_option('account_nickname'), account))
			else:
				sortedlist.append((self.settings.get_option('steam_username'), account))

		for account in sorted(sortedlist):
			self.settings.set_section(account[1])
			accountname = account[0]
			commandLinkButton = QtGui.QCommandLinkButton(self)
			commandLinkButton.setObjectName(self.settings.get_option('steam_username'))
			icon = QtGui.QIcon()
			if ui_account_box_icon != '':
				icon.addPixmap(QtGui.QPixmap(ui_account_box_icon))
			else:
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			commandLinkButton.setIcon(icon)
			commandLinkButton.setIconSize(QtCore.QSize(ui_account_box_icon_size, ui_account_box_icon_size))
			commandLinkButton.setCheckable(True)
			commandLinkButton.setChecked(accountname in checkedbuttons or self.settings.get_option('steam_username') in self.chosenGroupAccounts)
			self.settings.set_section('Settings')
			commandLinkButton.setStyleSheet('font: %spt "TF2 Build";' % ui_account_box_font_size)
			commandLinkButton.setText(accountname)
			self.accountButtons.append(commandLinkButton)
			self.gridLayout.addWidget(commandLinkButton, row, column, 1, 1)
			column += 1
			if column == numperrow:
				row += 1
				column = 0

	def mousePressEvent(self, event):
		button = event.button()
		# uncheck all account boxes on mouse right click
		if button == 2:
			for account in self.accountButtons:
				account.setChecked(False)
	
	def SelectAllAccounts(self):
		for account in self.accountButtons:
			account.setChecked(True)
	
	def returnSelectedAccounts(self):
		selectedList = []
		for account in self.accountButtons:
			if account.isChecked():
				selectedList.append(str(account.objectName()))
		self.emit(QtCore.SIGNAL('returnedSelectedAccounts(PyQt_PyObject)'), selectedList)
	
	def openAccountDialog(self, editAccount=False):
		if editAccount:
			checkedbuttons = []
			for widget in self.accountButtons:
				if widget.isChecked():
					checkedbuttons.append('Account-' + str(widget.objectName()))
			if len(checkedbuttons) == 0:
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to edit')
			else:
				dialogWindow = AccountDialogWindow(checkedbuttons)
				dialogWindow.setModal(True)
				dialogWindow.exec_()
				self.updateAccountBoxes()
		else:
			dialogWindow = AccountDialogWindow()
			dialogWindow.setModal(True)
			dialogWindow.exec_()
			self.updateAccountBoxes()

	def deleteAccounts(self):
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.objectName()))
		if len(checkedbuttons) == 0:
			QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to delete')
		else:
			reply = QtGui.QMessageBox.warning(self, 'Warning', 'Are you sure to want to delete these accounts?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				for account in checkedbuttons:
					self.settings.set_section('Account-' + account)
					self.settings.remove_section()
				self.updateAccountBoxes()
	
	def selectGroups(self):
		dialogWindow = GroupsDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.chosenGroupAccounts = dialogWindow.returnAccounts()
		self.updateAccountBoxes()
	
	def startUpAccounts(self, action):
		self.settings.set_section('Settings')
		easy_sandbox_mode = self.settings.get_option('easy_sandbox_mode')
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.objectName()))
		if len(checkedbuttons) == 0:
			if action == 'idle':
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to idle')
			elif action == 'idle_unsandboxed':
				QtGui.QMessageBox.information(self, 'No account selected', 'Please select an account to idle')
			elif action == 'start_steam':
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to start Steam with')
			elif action == 'start_TF2':
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to start TF2 with')
		elif action == 'idle_unsandboxed' and len(checkedbuttons) > 1:
			QtGui.QMessageBox.information(self, 'Too many accounts selected', 'Please select one account to idle')
		elif easy_sandbox_mode == 'yes' and action != 'idle_unsandboxed' and not self.runAsAdmin():
					QtGui.QMessageBox.information(self, 'Easy sandbox mode requires admin', 'TF2Idle requires admin privileges to create/modify sandboxes. Please run the program as admin.')
		else:
			self.settings.set_section('Settings')
			steamlocation = self.settings.get_option('steam_location')
			secondary_steamapps_location = self.settings.get_option('secondary_steamapps_location')
			sandboxielocation = self.settings.get_option('sandboxie_location')
			steamlaunchcommand = self.settings.get_option('launch_options')
			for account in checkedbuttons:
				self.settings.set_section('Account-' + account)
				username = self.settings.get_option('steam_username')
				password = self.settings.get_option('steam_password')
				sandboxname = self.settings.get_option('sandbox_name')
				if self.settings.get_option('sandbox_install') == '' or easy_sandbox_mode == 'yes':
					sandbox_install = secondary_steamapps_location
				else:
					sandbox_install = self.settings.get_option('sandbox_install')

				if not self.sandboxieINIIsModified and easy_sandbox_mode == 'yes':
					Sandboxie.backupSandboxieINI()
					self.mainwindow.sandboxieINIHasBeenModified()

				if action == 'idle':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (sandbox_install, username, password, steamlaunchcommand)
					if easy_sandbox_mode == 'yes':
						self.commandthread.addSandbox('TF2Idle' + username)
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, 'TF2Idle' + username, command)
					else:
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)
				elif action == 'idle_unsandboxed':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (steamlocation, username, password, steamlaunchcommand)
				elif action == 'start_steam':
					command = r'"%s/Steam.exe" -login %s %s' % (sandbox_install, username, password)
					if easy_sandbox_mode == 'yes':
						self.commandthread.addSandbox('TF2Idle' + username)
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, 'TF2Idle' + username, command)
					else:
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)
				elif action == 'start_TF2':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440' % (sandbox_install, username, password)
					if easy_sandbox_mode == 'yes':
						self.commandthread.addSandbox('TF2Idle' + username)
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, 'TF2Idle' + username, command)
					else:
						command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)

				self.commandthread.runCommand(command)
	
	def openBackpack(self):
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.objectName()))
		if len(checkedbuttons) == 0:
			QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to view backpack')
		else:
			self.settings.set_section('Settings')
			backpack_viewer = self.settings.get_option('backpack_viewer')
			if backpack_viewer == 'OPTF2':
				url = 'http://optf2.com/tf2/user/%(ID)s'
			elif backpack_viewer == 'Steam':
				url = 'http://steamcommunity.com/id/%(ID)s/inventory'
			elif backpack_viewer == 'TF2B':
				url = 'http://tf2b.com/?id=%(ID)s'
			elif backpack_viewer == 'TF2Items':
				url = 'http://www.tf2items.com/id/%(ID)s'
			for account in checkedbuttons:
				self.settings.set_section('Account-' + account)	
				webbrowser.open(url % {'ID': self.settings.get_option('steam_vanityid')})
	
	def modifySandboxes(self, action):
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.objectName()))
		if len(checkedbuttons) == 0:
			if action == '/terminate':
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to terminate its sandbox')
			else:
				QtGui.QMessageBox.information(self, 'No accounts selected', 'Please select at least one account to delete its sandbox contents')
		else:
			self.settings.set_section('Settings')
			sandboxie_location = self.settings.get_option('sandboxie_location')
			for account in checkedbuttons:
				self.settings.set_section('Account-' + account)
				if self.settings.get_option('sandbox_name') != '':
					command = r'"%s/Start.exe" /box:%s %s' % (sandboxie_location, self.settings.get_option('sandbox_name'), action)
					returnCode = subprocess.call(command)

	def updateGCFs(self):
		def Dialog(title, message):
			QtGui.QMessageBox.information(self, title, message)

		self.thread = Worker()
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('returnMessage'), Dialog)
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('StartedCopyingGCFs'), curry(self.updateWindow, disableUpdateGCFs=True))
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('FinishedCopyingGCFs'), self.updateWindow)
		self.thread.start()
	
	def runAsAdmin(self):
		try:
			is_admin = os.getuid() == 0
		except AttributeError:
			is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		return is_admin

class AccountDialogWindow(QtGui.QDialog):
	def __init__(self, accounts=[], parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AccountDialog(self, accounts)

class GroupsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_GroupsDialog(self)
	
	def returnAccounts(self):
		return self.ui.returnAccounts()