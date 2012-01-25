import Config, os
from PyQt4 import QtCore, QtGui
from sets import Set

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

class Ui_GroupsDialog(object):
	def __init__(self, GroupsDialog):
		self.settings = Config.settings
		
		# Create dialog
		self.GroupsDialog = GroupsDialog
		self.GroupsDialog.setWindowModality(QtCore.Qt.NonModal)
		self.GroupsDialog.resize(250, 450)
		self.GroupsDialog.setMinimumSize(QtCore.QSize(self.GroupsDialog.width(), self.GroupsDialog.height()))
		self.GroupsDialog.setWindowTitle('Select groups')
		self.GroupsDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/select_group.png')))
		
		self.gridLayout = QtGui.QVBoxLayout(self.GroupsDialog)
		
		# Generate groups dict
		self.groupsDict = {}
		for account in list(Set(self.settings.get_sections()) - Set(['Settings'])):
			groups = self.settings.get_option(account, 'groups')
			groups = groups.split(',')
			for group in groups:
				if group == '':
					pass
				else:
					if group in self.groupsDict:
						self.groupsDict[group].append(self.settings.get_option(account, 'steam_username'))
					else:
						self.groupsDict[group] = []
						self.groupsDict[group].append(self.settings.get_option(account, 'steam_username'))
		
		# Add group checkboxes
		self.groupButtons = []
		if len(self.groupsDict) == 0:
			self.Label = QtGui.QLabel()
			self.Label.setText('You have no groups set up. Try adding an account to a group first.')
			self.Label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
			self.Label.setWordWrap(True)
			self.gridLayout.addWidget(self.Label)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			for group in self.groupsDict:
				self.commandLinkButton = QtGui.QCommandLinkButton()
				self.commandLinkButton.setText(group)
				self.commandLinkButton.setIcon(icon)
				# Display members of group
				membersString = ''
				for member in self.groupsDict[group]:
					membersString += member + '\n'
				self.commandLinkButton.setDescription(membersString)
				self.commandLinkButton.setCheckable(True)
				self.gridLayout.addWidget(self.commandLinkButton)
				self.groupButtons.append(self.commandLinkButton)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox()
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setCenterButtons(False)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.gridLayout.addWidget(self.buttonBox)
		
		# Signal connections
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), GroupsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(GroupsDialog)
		
		self.accountsList = []
	
	def accept(self):
		for button in self.groupButtons:
			if button.isChecked():
				self.accountsList += self.groupsDict[str(button.text())]
		self.GroupsDialog.close()

	def returnAccounts(self):
		return self.accountsList
		