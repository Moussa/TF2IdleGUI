import Config, subprocess
from PyQt4 import QtCore, QtGui
from sets import Set
from AccountDialog import Ui_AccountDialog
from SettingsDialog import Ui_SettingsDialog
from GroupsDialog import Ui_GroupsDialog

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

class Ui_MainWindow(object):
	def __init__(self, MainWindow):
		self.settings = Config.settings
	
		# Create MainWindow
		self.MainWindow = MainWindow
		self.MainWindow.setObjectName('MainWindow')
		self.MainWindow.resize(650, 410)
		self.MainWindow.setWindowTitle('TF2Idle')
		
		# Add Tool bar
		self.toolBar = QtGui.QToolBar(self.MainWindow)
		self.toolBar.setObjectName('toolBar')
		self.toolBar.setIconSize(QtCore.QSize(40, 40))
		self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.toolBar.setMovable(False)
		
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap('tf2logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		
		addAccountIcon = QtGui.QIcon()
		addAccountIcon.addPixmap(QtGui.QPixmap('images/add_account.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.addAccountAction = self.toolBar.addAction(addAccountIcon, 'Add account')
		QtCore.QObject.connect(self.addAccountAction, QtCore.SIGNAL('triggered()'), self.openAccountDialog)
		
		editAccountIcon = QtGui.QIcon()
		editAccountIcon.addPixmap(QtGui.QPixmap('images/edit_account.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.editAccountAction = self.toolBar.addAction(editAccountIcon, 'Edit account')
		QtCore.QObject.connect(self.editAccountAction, QtCore.SIGNAL('triggered()'), curry(self.openAccountDialog, editAccount=True))
		
		removeAccountIcon = QtGui.QIcon()
		removeAccountIcon.addPixmap(QtGui.QPixmap('images/remove_account.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.deleteAccountsAction = self.toolBar.addAction(removeAccountIcon, 'Delete account')
		QtCore.QObject.connect(self.deleteAccountsAction, QtCore.SIGNAL('triggered()'), self.deleteAccounts)
		
		selectGroupIcon = QtGui.QIcon()
		selectGroupIcon.addPixmap(QtGui.QPixmap('images/select_group.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.selectGroupsAction = self.toolBar.addAction(selectGroupIcon, 'Select Groups')
		QtCore.QObject.connect(self.selectGroupsAction, QtCore.SIGNAL('triggered()'), self.selectGroups)
		
		startIdleIcon = QtGui.QIcon()
		startIdleIcon.addPixmap(QtGui.QPixmap('images/start_idle.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.startIdleAction = self.toolBar.addAction(startIdleIcon, 'Start idling')
		QtCore.QObject.connect(self.startIdleAction, QtCore.SIGNAL('triggered()'), self.idleAccounts)
		
		startLogIcon = QtGui.QIcon()
		startLogIcon.addPixmap(QtGui.QPixmap('images/start_log.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.toolBar.addAction(startLogIcon, 'Start log dropper')
		
		self.MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)
		
		# Create layout widget and attach to MainWindow
		self.centralwidget = QtGui.QWidget(self.MainWindow)
		self.centralwidget.setObjectName('centralwidget')
		self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, self.MainWindow.width()-self.toolBar.width(), self.MainWindow.height()))
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setMargin(0)
		self.MainWindow.setCentralWidget(self.centralwidget)
		
		# Add menu bar
		self.menubar = QtGui.QMenuBar(self.MainWindow)
		self.menubar.setObjectName('menubar')
		self.MainWindow.setMenuBar(self.menubar)
		
		# Add status bar
		#self.statusbar = QtGui.QStatusBar(self.MainWindow)
		#self.statusbar.setObjectName('statusbar')
		#self.MainWindow.setStatusBar(self.statusbar)
		
		# Add File menu
		menu = self.addMenu('File')
		self.addSubMenu(menu, 'Settings', text='Settings', statustip='Open settings', shortcut='Ctrl+S', action={'trigger':'triggered()', 'action':self.openSettings})
		menu.addSeparator()
		self.addSubMenu(menu, 'Exit', text='Exit', statustip='Exit TF2Idle', shortcut='Ctrl+Q', action={'trigger':'triggered()', 'action':MainWindow.close})
		
		# Add About menu
		self.addMenu('About')
		
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
		
		self.accountButtons = []
		self.chosenGroupAccounts = []
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
		buttonheight = self.verticalLayoutWidget.height()/5
		
		for account in list(Set(self.settings.get_sections()) - Set(['Settings'])):
			self.settings.set_section(account)
			if self.settings.get_option('account_nickname') != '':
				accountname = self.settings.get_option('account_nickname')
			else:
				accountname = self.settings.get_option('steam_username')
			commandLinkButton = QtGui.QCommandLinkButton(self.verticalLayoutWidget)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap('images/account_icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			commandLinkButton.setIcon(icon)
			commandLinkButton.setIconSize(QtCore.QSize(45, 45))
			commandLinkButton.setGeometry(QtCore.QRect(column*self.verticalLayoutWidget.width()/numperrow, row*buttonheight, self.verticalLayoutWidget.width()/numperrow, buttonheight))
			commandLinkButton.setCheckable(True)
			# See why this doesn't work
			font = QtGui.QFont()
			#font.setFamily('TF2 Build')
			font.setPointSize(commandLinkButton.width()/18)
			commandLinkButton.setFont(font)
			commandLinkButton.setChecked(accountname in checkedbuttons or self.settings.get_option('steam_username') in self.chosenGroupAccounts)
			commandLinkButton.setObjectName(self.settings.get_option('steam_username'))
			commandLinkButton.setText(accountname)
			self.accountButtons.append(commandLinkButton)
			commandLinkButton.show()
			column += 1
			if column == numperrow:
				row += 1
				column = 0

	def addMenu(self, menuname):
		self.menu = QtGui.QMenu(self.menubar)
		self.menu.setObjectName('menu' + menuname)
		self.menu.setTitle(menuname)
		self.menubar.addAction(self.menu.menuAction())
		return self.menu
	
	def addSubMenu(self, menu, menuname, shortcut=None, text=None, tooltip=None, statustip=None, action=None):
		self.action = QtGui.QAction(self.MainWindow)
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
				QtGui.QMessageBox.information(self.MainWindow, 'No accounts selected', 'Please select at least one account to edit')
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
			QtGui.QMessageBox.information(self.MainWindow, 'No accounts selected', 'Please select at least one account to delete')
		else:
			reply = QtGui.QMessageBox.warning(self.MainWindow, 'Warning', 'Are you sure to want to delete these accounts?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
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
	
	def idleAccounts(self, unsandboxed=False):
		checkedbuttons = []
		for widget in self.accountButtons:
			if widget.isChecked():
				checkedbuttons.append(str(widget.objectName()))
		if len(checkedbuttons) == 0:
			QtGui.QMessageBox.information(self.MainWindow, 'No accounts selected', 'Please select at least one account to idle')
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
				
				steamlaunchcommand = r'"%s/Steam.exe" -login %s %s -applaunch 440 +exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest' % (steamlocation, username, password)
				command = r'"%s/Start.exe" /box:%s %s' % (sandboxielocation, sandboxname, steamlaunchcommand)
				
				if sandboxname == '' or unsandboxed:
					returnCode = subprocess.call(steamlaunchcommand)
				else:
					returnCode = subprocess.call(command)

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
