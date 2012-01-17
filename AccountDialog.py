import Config, os
from PyQt4 import QtCore, QtGui

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

class Ui_AccountDialog(object):
	def __init__(self, AccountDialog, accounts):
		self.settings = Config.settings
		self.accounts = accounts
		self.currentUsername = None
		self.settings.set_section('Settings')
		self.easy_sandbox_mode = self.settings.get_option('easy_sandbox_mode')
		
		# Create dialog
		self.AccountDialog = AccountDialog
		self.AccountDialog.setWindowModality(QtCore.Qt.NonModal)
		self.AccountDialog.resize(450, 350)
		self.AccountDialog.setMinimumSize(QtCore.QSize(self.AccountDialog.width(), self.AccountDialog.height()))
		self.AccountDialog.setWindowTitle('Account details')
		self.AccountDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/settings.png')))
		
		# Add layout widget
		self.gridLayoutWidget = QtGui.QWidget(self.AccountDialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 380, 280))
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(0)
		
		# Set fonts/styles
		sectionfont = QtGui.QFont()
		sectionfont.setBold(True)
		sectionfont.setWeight(75)
		
		greyoutfont = QtGui.QFont()
		greyoutfont.setItalic(True)
		greyoutstyle = 'background-color: rgb(225, 225, 225);'
		
		self.italicfont = QtGui.QFont()
		self.italicfont.setItalic(True)
		
		# Steam account section
		self.steamAccountLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamAccountLabel.setFont(sectionfont)
		self.steamAccountLabel.setText('Steam details')
		self.gridLayout.addWidget(self.steamAccountLabel, 0, 0, 1, 1)
		
		self.steamUsernameLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamUsernameLabel.setToolTip('Your Steam username')
		self.steamUsernameLabel.setText('Steam username:')
		self.gridLayout.addWidget(self.steamUsernameLabel, 1, 0, 1, 1)
		
		self.steamUsernameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.steamUsernameLineEdit.setFrame(True)
		self.steamUsernameLineEdit.setToolTip('Your Steam username')
		if len(self.accounts) > 1:
			self.steamUsernameLineEdit.setReadOnly(True)
			self.steamUsernameLineEdit.setFont(greyoutfont)
			self.steamUsernameLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.steamUsernameLineEdit, 1, 1, 1, 1)
		
		self.steamPasswordLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamPasswordLabel.setToolTip('Your Steam password')
		self.steamPasswordLabel.setText('Steam password:')
		self.gridLayout.addWidget(self.steamPasswordLabel, 2, 0, 1, 1)
		
		self.steamPasswordLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.steamPasswordLineEdit.setFrame(True)
		self.steamPasswordLineEdit.setToolTip('Your Steam password')
		if len(self.accounts) > 1:
			self.steamPasswordLineEdit.setReadOnly(True)
			self.steamPasswordLineEdit.setFont(greyoutfont)
			self.steamPasswordLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.steamPasswordLineEdit, 2, 1, 1, 1)
		
		self.steamVanityIDLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamVanityIDLabel.setToolTip('Your Steam vanity ID. eg. steamcommunity.com/id/<vanityID>. Optional, only if you wish to use the view backpack feature')
		self.steamVanityIDLabel.setText('Steam vanity ID:')
		self.gridLayout.addWidget(self.steamVanityIDLabel, 3, 0, 1, 1)
		
		self.steamVanityIDLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.steamVanityIDLineEdit.setFrame(True)
		self.steamVanityIDLineEdit.setToolTip('Your Steam vanity ID. eg. steamcommunity.com/id/<vanityID>. Optional, only if you wish to use the view backpack feature')
		if len(self.accounts) > 1:
			self.steamVanityIDLineEdit.setReadOnly(True)
			self.steamVanityIDLineEdit.setFont(greyoutfont)
			self.steamVanityIDLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.steamVanityIDLineEdit, 3, 1, 1, 1)
		
		self.nicknameLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.nicknameLabel.setToolTip('Your account nickname to display within TF2Idle. Optional')
		self.nicknameLabel.setText('Account nickname:')
		self.gridLayout.addWidget(self.nicknameLabel, 4, 0, 1, 1)
		
		self.nicknameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.nicknameLineEdit.setFrame(True)
		self.nicknameLineEdit.setToolTip('Your account nickname to display within TF2Idle. Optional')
		if len(self.accounts) > 1:
			self.nicknameLineEdit.setReadOnly(True)
			self.nicknameLineEdit.setFont(greyoutfont)
			self.nicknameLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.nicknameLineEdit, 4, 1, 1, 1)
		
		# Sandboxie section
		self.sandboxieLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.sandboxieLabel.setFont(sectionfont)
		self.sandboxieLabel.setText('Sandboxie')
		self.gridLayout.addWidget(self.sandboxieLabel, 5, 0, 1, 1)
		
		self.sandboxNameLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.sandboxNameLabel.setToolTip('The name of the Sandboxie sandbox to use with this account. Optional, only if you wish to use sandboxes')
		self.sandboxNameLabel.setText('Sandbox name:')
		self.gridLayout.addWidget(self.sandboxNameLabel, 6, 0, 1, 1)
		
		self.sandboxNameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.sandboxNameLineEdit.setFrame(True)
		self.sandboxNameLineEdit.setToolTip('The name of the Sandboxie sandbox to use with this account. Optional, only if you wish to use sandboxes')
		if self.easy_sandbox_mode == 'yes':
			self.sandboxNameLineEdit.setReadOnly(True)
			self.sandboxNameLineEdit.setFont(greyoutfont)
			self.sandboxNameLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.sandboxNameLineEdit, 6, 1, 1, 1)
		
		self.sandboxPathLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.sandboxPathLabel.setToolTip('The path to Steam.exe for this sandbox. Optional, only if you wish to use sandboxes')
		self.sandboxPathLabel.setText('Sandbox path:')
		self.gridLayout.addWidget(self.sandboxPathLabel, 7, 0, 1, 1)
		
		self.sandboxPathLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.sandboxPathLineEdit.setFrame(True)
		self.sandboxPathLineEdit.setToolTip('The path to Steam.exe for this sandbox. Optional, only if you wish to use sandboxes')
		if self.easy_sandbox_mode == 'yes':
			self.sandboxPathLineEdit.setReadOnly(True)
			self.sandboxPathLineEdit.setFont(greyoutfont)
			self.sandboxPathLineEdit.setStyleSheet(greyoutstyle)
		self.gridLayout.addWidget(self.sandboxPathLineEdit, 7, 1, 1, 1)
		
		self.sandboxPathButton = QtGui.QPushButton(self.gridLayoutWidget)
		self.sandboxPathButton.setText('..')
		self.sandboxPathButton.setMaximumSize(QtCore.QSize(30, 20))
		self.gridLayout.addWidget(self.sandboxPathButton, 7, 2, 1, 1)
		
		# Other section
		self.otherLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.otherLabel.setFont(sectionfont)
		self.otherLabel.setText('Other')
		self.gridLayout.addWidget(self.otherLabel, 8, 0, 1, 1)
		
		self.groupsLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.groupsLabel.setToolTip('Groups this account is a member of. Optional, only if you wish to use the groups feature')
		self.groupsLabel.setText('Groups:')
		self.gridLayout.addWidget(self.groupsLabel, 9, 0, 1, 1)
		
		self.groupsLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.groupsLineEdit.setFrame(True)
		self.groupsLineEdit.setToolTip('Groups this account is a member of. Optional, only if you wish to use the groups feature')
		self.gridLayout.addWidget(self.groupsLineEdit, 9, 1, 1, 1)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self.AccountDialog)
		self.buttonBox.setGeometry(QtCore.QRect(60, 300, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		
		# Signal connections
		if self.easy_sandbox_mode == 'no':
			QtCore.QObject.connect(self.sandboxPathButton, QtCore.SIGNAL('clicked()'), self.getDirectory)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), self.AccountDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(self.AccountDialog)

		if len(self.accounts) != 0:
			self.populateDetails()
		
	def getDirectory(self):
		filepath = str(QtGui.QFileDialog.getExistingDirectory(self.gridLayoutWidget, 'Select Directory'))
		self.sandboxPathLineEdit.setText(filepath)
	
	def accept(self):
		steam_username = str(self.steamUsernameLineEdit.text())
		steam_password = str(self.steamPasswordLineEdit.text())
		steam_vanityid = str(self.steamVanityIDLineEdit.text())
		account_nickname = str(self.nicknameLineEdit.text())
		sandbox_name = str(self.sandboxNameLineEdit.text())
		sandbox_install = str(self.sandboxPathLineEdit.text())
		groups = str(self.groupsLineEdit.text())

		if steam_username == '':
			QtGui.QMessageBox.warning(self.AccountDialog, 'Error', 'Please enter a Steam username')
		elif steam_password == '':
			QtGui.QMessageBox.warning(self.AccountDialog, 'Error', 'Please enter a Steam password')
		elif len(self.accounts) == 0 or len(self.accounts) == 1:
			if self.settings.has_section('Account-' + steam_username) and (len(self.accounts) == 0 or (self.currentUsername != steam_username and len(self.accounts) == 1)):
				QtGui.QMessageBox.warning(self.AccountDialog, 'Error', 'Account already exists')
			else:
				if steam_vanityid == '': # Try steam username as vanity ID
					steam_vanityid = steam_username
				groups_string = ''
				if groups != '':
					groups_list = groups.split(',')
					# Remove trailing whitespaces from group names
					for group in groups_list:
						groups_string += group.strip() + ','
					# Remove trailing ,
					groups_string = groups_string[:-1]
				if len(self.accounts) == 1 and self.currentUsername != steam_username:
					self.settings.set_section('Account-' + self.currentUsername)
					self.settings.remove_section()
				self.settings.set_section('Account-' + steam_username)
				if len(self.accounts) == 0 or (len(self.accounts) == 1 and not self.settings.has_section('Account-' + steam_username)):
					self.settings.add_section()
				self.settings.set_option('steam_username', steam_username)
				self.settings.set_option('steam_password', steam_password)
				self.settings.set_option('steam_vanityid', steam_vanityid)
				self.settings.set_option('account_nickname', account_nickname)
				if self.easy_sandbox_mode == 'yes':
					if not self.settings.has_option('sandbox_name'):
						self.settings.set_option('sandbox_name', '')
					if not self.settings.has_option('sandbox_install'):
						self.settings.set_option('sandbox_install', '')
				else:
					self.settings.set_option('sandbox_name', sandbox_name)
					self.settings.set_option('sandbox_install', sandbox_install)
				self.settings.set_option('groups', groups_string)
				self.AccountDialog.close()
		else:
			for account in self.accounts:
				self.settings.set_section(account)
				if self.easy_sandbox_mode == 'no':
					self.settings.set_option('sandbox_name', sandbox_name)
					self.settings.set_option('sandbox_install', sandbox_install)
				self.settings.set_option('groups', groups)
			self.AccountDialog.close()
		
	def populateDetails(self):
		self.settings.set_section(self.accounts[0])
		if len(self.accounts) > 1:
			self.steamUsernameLineEdit.setText('Multiple values')
			self.steamPasswordLineEdit.setText('Multiple values')
			self.steamVanityIDLineEdit.setText('Multiple values')
			self.nicknameLineEdit.setText('Multiple values')
			if self.accountCommonValue('sandbox_name'):
				self.sandboxNameLineEdit.setText(self.settings.get_option('sandbox_name'))
			else:
				self.sandboxNameLineEdit.setText('Multiple values')
				self.sandboxNameLineEdit.setFont(self.italicfont)
			if self.accountCommonValue('sandbox_install'):
				self.sandboxPathLineEdit.setText(self.settings.get_option('sandbox_install'))
			else:
				self.sandboxPathLineEdit.setText('Multiple values')
				self.groupsLineEdit.setFont(self.italicfont)
			if self.accountCommonValue('groups'):
				self.groupsLineEdit.setText(self.settings.get_option('groups'))
			else:
				self.groupsLineEdit.setText('Multiple values')
				self.groupsLineEdit.setFont(self.italicfont)
		else:
			self.steamUsernameLineEdit.setText(self.settings.get_option('steam_username'))
			self.steamPasswordLineEdit.setText(self.settings.get_option('steam_password'))
			self.steamVanityIDLineEdit.setText(self.settings.get_option('steam_vanityid'))
			self.nicknameLineEdit.setText(self.settings.get_option('account_nickname'))
			if self.easy_sandbox_mode == 'yes':
				self.sandboxNameLineEdit.setText('Easy sandbox mode')
				self.sandboxPathLineEdit.setText('Easy sandbox mode')
			else:
				self.sandboxNameLineEdit.setText(self.settings.get_option('sandbox_name'))
				self.sandboxPathLineEdit.setText(self.settings.get_option('sandbox_install'))
			self.groupsLineEdit.setText(self.settings.get_option('groups'))

			self.currentUsername = self.settings.get_option('steam_username')
	
	def accountCommonValue(self, option):
		self.settings.set_section(self.accounts[0])
		value = sorted(self.settings.get_option(option).split(','))
		for account in self.accounts[1:]:
			self.settings.set_section(account)
			if sorted(self.settings.get_option(option).split(',')) != value:
				return False
		return True