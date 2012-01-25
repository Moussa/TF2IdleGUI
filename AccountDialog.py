import Config, os
from PyQt4 import QtCore, QtGui
from sets import Set

accountColourList = ['32CD32', '00BFFF', 'FF0000', 'FFD700', 'FF00FF', 'B0E0E6', 'FFFFFF', 'C0C0C0']

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
		self.easy_sandbox_mode = self.settings.get_option('Settings', 'easy_sandbox_mode')
		
		# Create dialog
		self.AccountDialog = AccountDialog
		self.AccountDialog.setWindowModality(QtCore.Qt.NonModal)
		self.AccountDialog.resize(450, 350)
		self.AccountDialog.setMinimumSize(QtCore.QSize(self.AccountDialog.width(), self.AccountDialog.height()))
		self.AccountDialog.setWindowTitle('Account details')
		self.AccountDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/settings.png')))
		
		self.vBoxLayout = QtGui.QVBoxLayout(self.AccountDialog)
		
		# Set fonts/styles
		greyoutfont = QtGui.QFont()
		greyoutfont.setItalic(True)
		greyoutstyle = 'background-color: rgb(225, 225, 225);'
		
		self.italicfont = QtGui.QFont()
		self.italicfont.setItalic(True)
		
		titleStyle = "QGroupBox {font-weight: bold;}"
		
		# Steam account section
		self.steamAccountGroupBox = QtGui.QGroupBox(self.AccountDialog)
		self.steamAccountGroupBox.setStyleSheet(titleStyle)
		self.steamAccountGroupBox.setTitle('Steam')
		
		self.vBoxLayout.addWidget(self.steamAccountGroupBox)
		
		self.steamAccountGroupBoxLayout = QtGui.QGridLayout(self.steamAccountGroupBox)
		
		self.steamUsernameLabel = QtGui.QLabel(self.steamAccountGroupBox)
		self.steamUsernameLabel.setToolTip('Your Steam username')
		self.steamUsernameLabel.setText('Steam username:')
		self.steamAccountGroupBoxLayout.addWidget(self.steamUsernameLabel, 0, 0, 1, 1)
		
		self.steamUsernameLineEdit = QtGui.QLineEdit()
		self.steamUsernameLineEdit.setFrame(True)
		self.steamUsernameLineEdit.setToolTip('Your Steam username')
		if len(self.accounts) > 1:
			self.steamUsernameLineEdit.setReadOnly(True)
			self.steamUsernameLineEdit.setFont(greyoutfont)
			self.steamUsernameLineEdit.setStyleSheet(greyoutstyle)
		self.steamAccountGroupBoxLayout.addWidget(self.steamUsernameLineEdit, 0, 1, 1, 1)
		
		self.steamPasswordLabel = QtGui.QLabel(self.steamAccountGroupBox)
		self.steamPasswordLabel.setToolTip('Your Steam password')
		self.steamPasswordLabel.setText('Steam password:')
		self.steamAccountGroupBoxLayout.addWidget(self.steamPasswordLabel, 1, 0, 1, 1)
		
		self.steamPasswordLineEdit = QtGui.QLineEdit()
		self.steamPasswordLineEdit.setFrame(True)
		self.steamPasswordLineEdit.setToolTip('Your Steam password')
		if len(self.accounts) > 1:
			self.steamPasswordLineEdit.setReadOnly(True)
			self.steamPasswordLineEdit.setFont(greyoutfont)
			self.steamPasswordLineEdit.setStyleSheet(greyoutstyle)
		self.steamAccountGroupBoxLayout.addWidget(self.steamPasswordLineEdit, 1, 1, 1, 1)
		
		self.steamVanityIDLabel = QtGui.QLabel(self.steamAccountGroupBox)
		self.steamVanityIDLabel.setToolTip('Your Steam vanity ID. eg. steamcommunity.com/id/<vanityID>. Optional, only if you wish to use the view backpack feature')
		self.steamVanityIDLabel.setText('Steam vanity ID:')
		self.steamAccountGroupBoxLayout.addWidget(self.steamVanityIDLabel, 2, 0, 1, 1)
		
		self.steamVanityIDLineEdit = QtGui.QLineEdit()
		self.steamVanityIDLineEdit.setFrame(True)
		self.steamVanityIDLineEdit.setToolTip('Your Steam vanity ID. eg. steamcommunity.com/id/<vanityID>. Optional, only if you wish to use the view backpack feature')
		if len(self.accounts) > 1:
			self.steamVanityIDLineEdit.setReadOnly(True)
			self.steamVanityIDLineEdit.setFont(greyoutfont)
			self.steamVanityIDLineEdit.setStyleSheet(greyoutstyle)
		self.steamAccountGroupBoxLayout.addWidget(self.steamVanityIDLineEdit, 2, 1, 1, 1)
		
		self.nicknameLabel = QtGui.QLabel(self.steamAccountGroupBox)
		self.nicknameLabel.setToolTip('Your account nickname to display within TF2Idle. Optional')
		self.nicknameLabel.setText('Account nickname:')
		self.steamAccountGroupBoxLayout.addWidget(self.nicknameLabel, 3, 0, 1, 1)
		
		self.nicknameLineEdit = QtGui.QLineEdit()
		self.nicknameLineEdit.setFrame(True)
		self.nicknameLineEdit.setToolTip('Your account nickname to display within TF2Idle. Optional')
		if len(self.accounts) > 1:
			self.nicknameLineEdit.setReadOnly(True)
			self.nicknameLineEdit.setFont(greyoutfont)
			self.nicknameLineEdit.setStyleSheet(greyoutstyle)
		self.steamAccountGroupBoxLayout.addWidget(self.nicknameLineEdit, 3, 1, 1, 1)
		
		# Sandboxie section
		self.sandboxieGroupBox = QtGui.QGroupBox(self.AccountDialog)
		self.sandboxieGroupBox.setStyleSheet(titleStyle)
		self.sandboxieGroupBox.setTitle('Sandboxie')
		
		self.vBoxLayout.addWidget(self.sandboxieGroupBox)
		
		self.sandboxieGroupBoxLayout = QtGui.QGridLayout(self.sandboxieGroupBox)
		
		self.sandboxNameLabel = QtGui.QLabel(self.sandboxieGroupBox)
		self.sandboxNameLabel.setToolTip('The name of the Sandboxie sandbox to use with this account. Optional, only if you wish to use sandboxes')
		self.sandboxNameLabel.setText('Sandbox name:')
		self.sandboxieGroupBoxLayout.addWidget(self.sandboxNameLabel, 0, 0, 1, 1)
		
		self.sandboxNameLineEdit = QtGui.QLineEdit()
		self.sandboxNameLineEdit.setFrame(True)
		self.sandboxNameLineEdit.setToolTip('The name of the Sandboxie sandbox to use with this account. Optional, only if you wish to use sandboxes')
		if self.easy_sandbox_mode == 'yes':
			self.sandboxNameLineEdit.setReadOnly(True)
			self.sandboxNameLineEdit.setFont(greyoutfont)
			self.sandboxNameLineEdit.setText('Easy sandbox mode')
			self.sandboxNameLineEdit.setStyleSheet(greyoutstyle)
		self.sandboxieGroupBoxLayout.addWidget(self.sandboxNameLineEdit, 0, 1, 1, 1)
		
		self.sandboxPathLabel = QtGui.QLabel(self.sandboxieGroupBox)
		self.sandboxPathLabel.setToolTip('The path to Steam.exe for this sandbox. Optional, only if you wish to use sandboxes')
		self.sandboxPathLabel.setText('Sandbox path:')
		self.sandboxieGroupBoxLayout.addWidget(self.sandboxPathLabel, 1, 0, 1, 1)
		
		self.sandboxPathLineEdit = QtGui.QLineEdit()
		self.sandboxPathLineEdit.setFrame(True)
		self.sandboxPathLineEdit.setToolTip('The path to Steam.exe for this sandbox. Optional, only if you wish to use sandboxes')
		if self.easy_sandbox_mode == 'yes':
			self.sandboxPathLineEdit.setReadOnly(True)
			self.sandboxPathLineEdit.setFont(greyoutfont)
			self.sandboxPathLineEdit.setText('Easy sandbox mode')
			self.sandboxPathLineEdit.setStyleSheet(greyoutstyle)
		self.sandboxieGroupBoxLayout.addWidget(self.sandboxPathLineEdit, 1, 1, 1, 1)
		
		self.sandboxPathButton = QtGui.QPushButton()
		self.sandboxPathButton.setText('..')
		self.sandboxPathButton.setMaximumSize(QtCore.QSize(30, 20))
		self.sandboxieGroupBoxLayout.addWidget(self.sandboxPathButton, 1, 2, 1, 1)
		
		# Other section
		self.otherGroupBox = QtGui.QGroupBox(self.AccountDialog)
		self.otherGroupBox.setStyleSheet(titleStyle)
		self.otherGroupBox.setTitle('Other')
		
		self.vBoxLayout.addWidget(self.otherGroupBox)
		
		self.otherGroupBoxLayout = QtGui.QGridLayout(self.otherGroupBox)
		
		self.groupsLabel = QtGui.QLabel(self.otherGroupBox)
		self.groupsLabel.setToolTip('Groups this account is a member of. Optional, only if you wish to use the groups feature')
		self.groupsLabel.setText('Groups:')
		self.otherGroupBoxLayout.addWidget(self.groupsLabel, 0, 0, 1, 1)
		
		self.groupsLineEdit = QtGui.QLineEdit()
		self.groupsLineEdit.setFrame(True)
		self.groupsLineEdit.setToolTip('Groups this account is a member of. Optional, only if you wish to use the groups feature')
		self.otherGroupBoxLayout.addWidget(self.groupsLineEdit, 0, 1, 1, 1)
		
		if len(self.accounts) < 2:
			self.dropLogColourLabel = QtGui.QLabel(self.otherGroupBox)
			self.dropLogColourLabel.setToolTip('The account colour used in the drop log feature')
			self.dropLogColourLabel.setText('Drop log colour:')
			self.otherGroupBoxLayout.addWidget(self.dropLogColourLabel, 1, 0, 1, 1)

			self.dropLogColourFrame = QtGui.QLineEdit()
			self.dropLogColourFrame.setReadOnly(True)
			if len(self.accounts) == 0:
				self.dropLogColour = accountColourList[len(list(Set(self.settings.get_sections()) - Set(['Settings']))) % len(accountColourList)]
				self.dropLogColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogColour)
			self.otherGroupBoxLayout.addWidget(self.dropLogColourFrame, 1, 1, 1, 1)

			self.dropLogColourButton = QtGui.QPushButton()
			self.dropLogColourButton.setText('..')
			self.dropLogColourButton.setMaximumSize(QtCore.QSize(30, 20))
			self.otherGroupBoxLayout.addWidget(self.dropLogColourButton, 1, 2, 1, 1)

		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self.AccountDialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.vBoxLayout.addWidget(self.buttonBox)

		# Set mininmum label lengths on all groupboxes to align right hand side widgets
		self.setMinLabelLength(self.AccountDialog)

		# Signal connections
		if self.easy_sandbox_mode == 'no':
			QtCore.QObject.connect(self.sandboxPathButton, QtCore.SIGNAL('clicked()'), self.getDirectory)
		if len(self.accounts) < 2:
			QtCore.QObject.connect(self.dropLogColourButton, QtCore.SIGNAL('clicked()'), self.getColour)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), self.AccountDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(self.AccountDialog)

		if len(self.accounts) != 0:
			self.populateDetails()

	def setMinLabelLength(self, dialog):
		groupboxes = dialog.findChildren(QtGui.QGroupBox)
		labels = []
		for groupbox in groupboxes:
			labels.extend(groupbox.findChildren(QtGui.QLabel))
		largestwidth = labels[0].sizeHint().width()
		for label in labels[1:]:
			if label.sizeHint().width() > largestwidth:
				largestwidth = label.sizeHint().width()
		for label in labels:
			label.setMinimumSize(QtCore.QSize(largestwidth, 0))
		
	def getDirectory(self):
		filepath = str(QtGui.QFileDialog.getExistingDirectory(self.gridLayoutWidget, 'Select Directory'))
		self.sandboxPathLineEdit.setText(filepath)
	
	def getColour(self):
		colour = QtGui.QColorDialog.getColor()
		if colour.isValid():
			self.dropLogColourFrame.setStyleSheet('background-color: %s;' % colour.name())
			self.dropLogColour = str(colour.name())[1:]
	
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
					self.settings.remove_section('Account-' + self.currentUsername)
				if len(self.accounts) == 0 or (len(self.accounts) == 1 and not self.settings.has_section('Account-' + steam_username)):
					self.settings.add_section('Account-' + steam_username)
				self.settings.set_option('Account-' + steam_username, 'steam_username', steam_username)
				self.settings.set_option('Account-' + steam_username, 'steam_password', steam_password)
				self.settings.set_option('Account-' + steam_username, 'steam_vanityid', steam_vanityid)
				self.settings.set_option('Account-' + steam_username, 'account_nickname', account_nickname)
				if self.easy_sandbox_mode == 'yes':
					if not self.settings.has_option('Account-' + steam_username, 'sandbox_name'):
						self.settings.set_option('Account-' + steam_username, 'sandbox_name', '')
					if not self.settings.has_option('Account-' + steam_username, 'sandbox_install'):
						self.settings.set_option('Account-' + steam_username, 'sandbox_install', '')
				else:
					self.settings.set_option('Account-' + steam_username, 'sandbox_name', sandbox_name)
					self.settings.set_option('Account-' + steam_username, 'sandbox_install', sandbox_install)
				self.settings.set_option('Account-' + steam_username, 'groups', groups_string)
				self.settings.set_option('Account-' + steam_username, 'ui_log_colour', self.dropLogColour)
				self.AccountDialog.close()
		else:
			for account in self.accounts:
				if self.easy_sandbox_mode == 'no':
					self.settings.set_option(account, 'sandbox_name', sandbox_name)
					self.settings.set_option(account, 'sandbox_install', sandbox_install)
				self.settings.set_option(account, 'groups', groups)
			self.AccountDialog.close()
		
	def populateDetails(self):
		if len(self.accounts) > 1:
			self.steamUsernameLineEdit.setText('Multiple values')
			self.steamPasswordLineEdit.setText('Multiple values')
			self.steamVanityIDLineEdit.setText('Multiple values')
			self.nicknameLineEdit.setText('Multiple values')
			if self.accountCommonValue('sandbox_name'):
				self.sandboxNameLineEdit.setText(self.settings.get_option(self.accounts[0], 'sandbox_name'))
			else:
				self.sandboxNameLineEdit.setText('Multiple values')
				self.sandboxNameLineEdit.setFont(self.italicfont)
			if self.accountCommonValue('sandbox_install'):
				self.sandboxPathLineEdit.setText(self.settings.get_option(self.accounts[0], 'sandbox_install'))
			else:
				self.sandboxPathLineEdit.setText('Multiple values')
				self.groupsLineEdit.setFont(self.italicfont)
			if self.accountCommonValue('groups'):
				self.groupsLineEdit.setText(self.settings.get_option(self.accounts[0], 'groups'))
			else:
				self.groupsLineEdit.setText('Multiple values')
				self.groupsLineEdit.setFont(self.italicfont)
		else:
			self.steamUsernameLineEdit.setText(self.settings.get_option(self.accounts[0], 'steam_username'))
			self.steamPasswordLineEdit.setText(self.settings.get_option(self.accounts[0], 'steam_password'))
			self.steamVanityIDLineEdit.setText(self.settings.get_option(self.accounts[0], 'steam_vanityid'))
			self.nicknameLineEdit.setText(self.settings.get_option(self.accounts[0], 'account_nickname'))
			if self.easy_sandbox_mode == 'yes':
				self.sandboxNameLineEdit.setText('Easy sandbox mode')
				self.sandboxPathLineEdit.setText('Easy sandbox mode')
			else:
				self.sandboxNameLineEdit.setText(self.settings.get_option(self.accounts[0], 'sandbox_name'))
				self.sandboxPathLineEdit.setText(self.settings.get_option(self.accounts[0], 'sandbox_install'))
			self.groupsLineEdit.setText(self.settings.get_option(self.accounts[0], 'groups'))

			self.currentUsername = self.settings.get_option(self.accounts[0], 'steam_username')

			self.dropLogColour = self.settings.get_option(self.accounts[0], 'ui_log_colour')
			self.dropLogColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogColour)
	
	def accountCommonValue(self, option):
		value = sorted(self.settings.get_option(self.accounts[0], option).split(','))
		for account in self.accounts[1:]:
			if sorted(self.settings.get_option(account, option).split(',')) != value:
				return False
		return True