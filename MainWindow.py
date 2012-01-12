import Config, subprocess, webbrowser, shutil, os, threading
from PyQt4 import QtCore, QtGui
from sets import Set
from AccountDialog import Ui_AccountDialog
from SettingsDialog import Ui_SettingsDialog
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

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.settings = Config.settings
		self.toolBars = []
		self.accountButtons = []
		self.chosenGroupAccounts = []
		
		# Create MainWindow
		self.setObjectName('MainWindow')
		self.settings.set_section('Settings')
		windowXSize, windowYSize = eval(self.settings.get_option('ui_window_size'))
		self.resize(windowXSize, windowYSize)
		self.setWindowTitle('TF2Idle')
		self.setWindowIcon(QtGui.QIcon(returnResourcePath('images/tf2idle.png')))

		self.updateWindow()
	
	def updateWindow(self, disableUpdateGCFs=False):
		# Clear toolbars first
		for toolbar in self.toolBars:
			toolbar.close()
			del toolbar

		# Create vertical toolbar
		self.vtoolBar = QtGui.QToolBar(self)
		self.vtoolBar.setObjectName('vtoolBar')
		self.vtoolBar.setIconSize(QtCore.QSize(40, 40))
		self.vtoolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.vtoolBar.setMovable(False)
		
		# Create horizontal toolbar
		self.htoolBar = QtGui.QToolBar(self)
		self.htoolBar.setObjectName('htoolBar')
		self.htoolBar.setIconSize(QtCore.QSize(40, 40))
		self.htoolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.htoolBar.setMovable(False)
		
		# Add toolbars to toolbar list so can be deleted when MainWindow is refreshed
		self.toolBars.append(self.vtoolBar)
		self.toolBars.append(self.htoolBar)
		
		# Add vertical toolbar actions
		addAccountIcon = QtGui.QIcon()
		addAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/add_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.addAccountAction = self.vtoolBar.addAction(addAccountIcon, 'Add account')
		QtCore.QObject.connect(self.addAccountAction, QtCore.SIGNAL('triggered()'), self.openAccountDialog)
		
		editAccountIcon = QtGui.QIcon()
		editAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/edit_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.editAccountAction = self.vtoolBar.addAction(editAccountIcon, 'Edit account')
		QtCore.QObject.connect(self.editAccountAction, QtCore.SIGNAL('triggered()'), curry(self.openAccountDialog, editAccount=True))
		
		removeAccountIcon = QtGui.QIcon()
		removeAccountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/remove_account.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.deleteAccountsAction = self.vtoolBar.addAction(removeAccountIcon, 'Delete account')
		QtCore.QObject.connect(self.deleteAccountsAction, QtCore.SIGNAL('triggered()'), self.deleteAccounts)
		
		selectGroupIcon = QtGui.QIcon()
		selectGroupIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/select_group.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.selectGroupsAction = self.vtoolBar.addAction(selectGroupIcon, 'Select Groups')
		QtCore.QObject.connect(self.selectGroupsAction, QtCore.SIGNAL('triggered()'), self.selectGroups)
		
		viewBackpackIcon = QtGui.QIcon()
		viewBackpackIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/backpack.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.viewBackpackAction = self.vtoolBar.addAction(viewBackpackIcon, 'View backpack')
		QtCore.QObject.connect(self.viewBackpackAction, QtCore.SIGNAL('triggered()'), self.openBackpack)
		
		# Add horizontal toolbar actions
		
		startIdleIcon = QtGui.QIcon()
		startIdleIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_idle.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startIdleAction = self.htoolBar.addAction(startIdleIcon, 'Start idling')
		QtCore.QObject.connect(self.startIdleAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='idle'))
		
		startIdleUnsandboxedIcon = QtGui.QIcon()
		startIdleUnsandboxedIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_idle_unsandboxed.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startIdleUnsandboxedAction = self.htoolBar.addAction(startIdleUnsandboxedIcon, 'Start idling (no sandbox)')
		QtCore.QObject.connect(self.startIdleUnsandboxedAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='idle_unsandboxed'))
		
		startTF2Icon = QtGui.QIcon()
		startTF2Icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_tf2.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startTF2Action = self.htoolBar.addAction(startTF2Icon, 'Start TF2')
		QtCore.QObject.connect(self.startTF2Action, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='start_TF2'))
		
		startSteamIcon = QtGui.QIcon()
		startSteamIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_steam.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startSteamAction = self.htoolBar.addAction(startSteamIcon, 'Start Steam')
		QtCore.QObject.connect(self.startSteamAction, QtCore.SIGNAL('triggered()'), curry(self.startUpAccounts, action='start_steam'))
		
		self.htoolBar.addSeparator()
		
		updateGCFsIcon = QtGui.QIcon()
		if not disableUpdateGCFs:
			updateGCFsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/update_gcfs.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.updateGCFsAction = self.htoolBar.addAction(updateGCFsIcon, 'Update GCFs')
			QtCore.QObject.connect(self.updateGCFsAction, QtCore.SIGNAL('triggered()'), self.updateGCFs)
		else:
			updateGCFsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/updating_gcfs.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.updateGCFsAction = self.htoolBar.addAction(updateGCFsIcon, 'Updating GCFs')
		
		terminateSandboxIcon = QtGui.QIcon()
		terminateSandboxIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/terminate_sandbox.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.terminateSandboxAction = self.htoolBar.addAction(terminateSandboxIcon, 'Terminate sandbox')
		QtCore.QObject.connect(self.terminateSandboxAction, QtCore.SIGNAL('triggered()'), curry(self.modifySandboxes, action='/terminate'))
		
		emptySandboxIcon = QtGui.QIcon()
		emptySandboxIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/delete_sandbox.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.emptySandboxAction = self.htoolBar.addAction(emptySandboxIcon, 'Empty sandbox')
		QtCore.QObject.connect(self.emptySandboxAction, QtCore.SIGNAL('triggered()'), curry(self.modifySandboxes, action='delete_sandbox'))
		
		self.htoolBar.addSeparator()
		
		startLogIcon = QtGui.QIcon()
		startLogIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/start_log.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.htoolBar.addAction(startLogIcon, 'Start drop log')
		
		# Attach toolbars to MainWindow
		self.addToolBar(QtCore.Qt.BottomToolBarArea, self.htoolBar)
		self.addToolBar(QtCore.Qt.RightToolBarArea, self.vtoolBar)
		
		self.centralwidget = QtGui.QWidget(self)
		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setMargin(0)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
		self.setCentralWidget(self.centralwidget)
		
		# Add menu bar
		self.menubar = QtGui.QMenuBar(self)
		self.menubar.setObjectName('menubar')
		self.setMenuBar(self.menubar)
		
		# Add File menu
		filemenu = self.addMenu('File')
		self.addSubMenu(filemenu, 'Settings', text='Settings', statustip='Open settings', shortcut='Ctrl+S', action={'trigger':'triggered()', 'action':self.openSettings})
		filemenu.addSeparator()
		self.addSubMenu(filemenu, 'Exit', text='Exit', statustip='Exit TF2Idle', shortcut='Ctrl+Q', action={'trigger':'triggered()', 'action':self.close})
		
		# Add About menu
		aboutmenu = self.addMenu('About')
		self.addSubMenu(aboutmenu, 'Credits', text='Credits', statustip='See credits', action={'trigger':'triggered()', 'action':self.showCredits})
		
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.updateAccountBoxes()

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
		
		for account in list(Set(self.settings.get_sections()) - Set(['Settings'])):
			self.settings.set_section(account)
			if self.settings.get_option('account_nickname') != '':
				accountname = self.settings.get_option('account_nickname')
			else:
				accountname = self.settings.get_option('steam_username')
			commandLinkButton = QtGui.QCommandLinkButton(self.centralwidget)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			commandLinkButton.setIcon(icon)
			commandLinkButton.setIconSize(QtCore.QSize(45, 45))
			commandLinkButton.setStyleSheet('font: 10pt "TF2 Build";')
			commandLinkButton.setCheckable(True)
			commandLinkButton.setChecked(accountname in checkedbuttons or self.settings.get_option('steam_username') in self.chosenGroupAccounts)
			commandLinkButton.setObjectName(self.settings.get_option('steam_username'))
			commandLinkButton.setText(accountname)
			self.accountButtons.append(commandLinkButton)
			self.gridLayout.addWidget(commandLinkButton, row, column, 1, 1)
			column += 1
			if column == numperrow:
				row += 1
				column = 0

	def closeEvent(self, event):
		self.settings.set_section('Settings')
		self.settings.set_option('ui_window_size', '(%s, %s)' % (self.width(), self.height()))

	def addMenu(self, menuname):
		self.menu = QtGui.QMenu(self.menubar)
		self.menu.setObjectName('menu' + menuname)
		self.menu.setTitle(menuname)
		self.menubar.addAction(self.menu.menuAction())
		return self.menu
	
	def addSubMenu(self, menu, menuname, shortcut=None, text=None, tooltip=None, statustip=None, action=None):
		self.action = QtGui.QAction(self)
		if shortcut:
			self.action.setShortcut(shortcut)
		self.action.setObjectName('action' + menuname)
		menu.addAction(self.action)
		if action:
			QtCore.QObject.connect(self.action, QtCore.SIGNAL(action['trigger']), action['action'])
		if text:
			self.action.setText(text)
		if tooltip:
			self.action.setToolTip(tooltip)
		if statustip:
			self.action.setStatusTip(statustip)
	
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
	
	def openSettings(self):
		dialogWindow = SettingsDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.updateAccountBoxes()
	
	def selectGroups(self):
		dialogWindow = GroupsDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.chosenGroupAccounts = dialogWindow.returnAccounts()
		self.updateAccountBoxes()
	
	def showCredits(self):
		about = QtGui.QMessageBox(self)
		about.setWindowTitle('Credits')
		about.setIconPixmap(QtGui.QPixmap(returnResourcePath('images/tf2idle.png')))
		about.setTextFormat(QtCore.Qt.RichText)
		about.setText("""<b>TF2Idle 1.0</b><br/><br/>Developed by <a href="http://steamcommunity.com/id/Moussekateer">Moussekateer</a>
						 <br/><br/>Thanks to <a href="http://steamcommunity.com/id/WindPower">WindPower</a> for his limitless Python knowledge.
						 <br/><br/>Thanks to <a href="http://steamcommunity.com/id/rjackson">RJackson</a> for contributing code to TF2Idle.
						 <br/><br/>Thanks to <a href="http://wiki.teamfortress.com">official TF2 wiki</a> for the \'borrowed\' icons.
						 <br/><br/>They are kredit to team.""")
		about.exec_()
	
	def startUpAccounts(self, action):
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
		else:
			for account in checkedbuttons:
				self.settings.set_section('Settings')
				steamlocation = self.settings.get_option('steam_location')
				sandboxielocation = self.settings.get_option('sandboxie_location')
				steamlaunchcommand = self.settings.get_option('launch_options')
				self.settings.set_section('Account-' + account)
				username = self.settings.get_option('steam_username')
				password = self.settings.get_option('steam_password')
				sandboxname = self.settings.get_option('sandbox_name')
				sandbox_install = self.settings.get_option('sandbox_install')
				
				if action == 'idle':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (sandbox_install, username, password, steamlaunchcommand)
					command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)
				if action == 'idle_unsandboxed':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440 %s' % (steamlocation, username, password, steamlaunchcommand)
				elif action == 'start_steam':
					command = r'"%s/Steam.exe" -login %s %s' % (sandbox_install, username, password)
					command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)
				elif action == 'start_TF2':
					command = r'"%s/Steam.exe" -login %s %s -applaunch 440' % (sandbox_install, username, password)
					command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, command)
				
				returnCode = subprocess.call(command)
	
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

class AccountDialogWindow(QtGui.QDialog):
	def __init__(self, accounts=[], parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AccountDialog(self, accounts)

class SettingsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_SettingsDialog(self)

class GroupsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_GroupsDialog(self)
	
	def returnAccounts(self):
		return self.ui.returnAccounts()