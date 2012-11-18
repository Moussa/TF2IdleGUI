import Config
from PyQt4 import QtCore, QtGui
from sets import Set

from Common import returnResourcePath

def compare_keys(x, y):
	try:
		x = int(x)
	except ValueError:
		xint = False
	else:
		xint = True
	try:
		y = int(y)
	except ValueError:
		if xint:
			return -1
		return cmp(x, y)
	else:
		if xint:
			return cmp(x, y)
		return 1

class GroupsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.settings = Config.settings
		
		# Create dialog
		self.setWindowModality(QtCore.Qt.NonModal)
		self.resize(250, 450)
		self.setMinimumSize(QtCore.QSize(self.width(), self.height()))
		self.setWindowTitle('Select groups')
		self.setWindowIcon(QtGui.QIcon(returnResourcePath('images/select_group.png')))

		self.gridLayout = QtGui.QVBoxLayout(self)

		self.scrollArea = QtGui.QScrollArea(self)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
		self.gridLayout.addWidget(self.scrollArea)
		
		self.scrollAreaWidgetContents = QtGui.QWidget()
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)

		self.widgetVerticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
		
		self.verticalLayout = QtGui.QVBoxLayout()
		self.widgetVerticalLayout.addLayout(self.verticalLayout)
		
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
			self.verticalLayout.addWidget(self.Label)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			for group in sorted(self.groupsDict, cmp = compare_keys):
				self.commandLinkButton = QtGui.QCommandLinkButton()
				self.commandLinkButton.setText(group)
				self.commandLinkButton.setIcon(icon)
				# Display members of group
				membersString = ''
				for member in sorted(self.groupsDict[group]):
					membersString += member + '\n'
				self.commandLinkButton.setDescription(membersString)
				self.commandLinkButton.setCheckable(True)
				self.verticalLayout.addWidget(self.commandLinkButton)
				self.groupButtons.append(self.commandLinkButton)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox()
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setCenterButtons(True)

		selectbutton = QtGui.QPushButton('Select', self)
		deselectbutton = QtGui.QPushButton('Deselect', self)
		cancelbutton = QtGui.QPushButton('Cancel', self)

		self.buttonBox.addButton(selectbutton, QtGui.QDialogButtonBox.ActionRole)
		self.buttonBox.addButton(deselectbutton, QtGui.QDialogButtonBox.ActionRole)
		self.buttonBox.addButton(cancelbutton, QtGui.QDialogButtonBox.RejectRole)

		self.gridLayout.addWidget(self.buttonBox)
		
		# Signal connections
		self.connect(selectbutton, QtCore.SIGNAL('clicked()'), self.select)
		self.connect(deselectbutton, QtCore.SIGNAL('clicked()'), self.deselect)
		self.connect(cancelbutton, QtCore.SIGNAL('clicked()'), self.reject)
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.accountsSelectList = []
		self.accountsDeselectList = []
	
	def select(self):
		for button in self.groupButtons:
			if button.isChecked():
				self.accountsSelectList += self.groupsDict[str(button.text())]
		self.close()

	def deselect(self):
		for button in self.groupButtons:
			if button.isChecked():
				self.accountsDeselectList += self.groupsDict[str(button.text())]
		self.close()

	def returnAccounts(self):
		return self.accountsSelectList, self.accountsDeselectList