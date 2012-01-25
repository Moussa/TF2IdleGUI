import Config, os
from PyQt4 import QtCore, QtGui

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

class Ui_LogEntriesDialog(object):
	def __init__(self, LogEntriesDialog):
		self.settings = Config.settings
		
		# Create dialog
		self.LogEntriesDialog = LogEntriesDialog
		self.LogEntriesDialog.setWindowModality(QtCore.Qt.NonModal)
		self.LogEntriesDialog.setWindowTitle('Log entries')
		self.LogEntriesDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/select_group.png')))
		
		self.vBoxLayout = QtGui.QVBoxLayout(self.LogEntriesDialog)
		
		# Add command link buttons
		self.systemCommandLinkButton = QtGui.QCommandLinkButton()
		self.systemCommandLinkButton.setText('System messages')
		icon = QtGui.QIcon(QtGui.QPixmap(returnResourcePath('images/settings.png')))
		self.systemCommandLinkButton.setIcon(icon)
		self.systemCommandLinkButton.setIconSize(QtCore.QSize(40,40))
		self.systemCommandLinkButton.setCheckable(True)
		self.vBoxLayout.addWidget(self.systemCommandLinkButton)

		self.hatsCommandLinkButton = QtGui.QCommandLinkButton()
		self.hatsCommandLinkButton.setText('Hats')
		icon = QtGui.QIcon(QtGui.QPixmap(returnResourcePath('images/hat.png')))
		self.hatsCommandLinkButton.setIcon(icon)
		self.hatsCommandLinkButton.setIconSize(QtCore.QSize(40,40))
		self.hatsCommandLinkButton.setCheckable(True)
		self.vBoxLayout.addWidget(self.hatsCommandLinkButton)
		
		self.weaponsCommandLinkButton = QtGui.QCommandLinkButton()
		self.weaponsCommandLinkButton.setText('Weapons')
		icon = QtGui.QIcon(QtGui.QPixmap(returnResourcePath('images/weapon.png')))
		self.weaponsCommandLinkButton.setIcon(icon)
		self.weaponsCommandLinkButton.setIconSize(QtCore.QSize(40,40))
		self.weaponsCommandLinkButton.setCheckable(True)
		self.vBoxLayout.addWidget(self.weaponsCommandLinkButton)
		
		self.toolsCommandLinkButton = QtGui.QCommandLinkButton()
		self.toolsCommandLinkButton.setText('Tools')
		icon = QtGui.QIcon(QtGui.QPixmap(returnResourcePath('images/tool.png')))
		self.toolsCommandLinkButton.setIcon(icon)
		self.toolsCommandLinkButton.setIconSize(QtCore.QSize(40,40))
		self.toolsCommandLinkButton.setCheckable(True)
		self.vBoxLayout.addWidget(self.toolsCommandLinkButton)
		
		self.cratesCommandLinkButton = QtGui.QCommandLinkButton()
		self.cratesCommandLinkButton.setText('Crates')
		icon = QtGui.QIcon(QtGui.QPixmap(returnResourcePath('images/crate.png')))
		self.cratesCommandLinkButton.setIcon(icon)
		self.cratesCommandLinkButton.setIconSize(QtCore.QSize(40,40))
		self.cratesCommandLinkButton.setCheckable(True)
		self.vBoxLayout.addWidget(self.cratesCommandLinkButton)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox()
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setCenterButtons(False)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.vBoxLayout.addWidget(self.buttonBox)
		
		# Signal connections
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), LogEntriesDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(self.LogEntriesDialog)

		self.populateDetails()
	
	def accept(self):
		toggles = ''

		if self.systemCommandLinkButton.isChecked():
			toggles += 'system,'
		if self.hatsCommandLinkButton.isChecked():
			toggles += 'hats,'
		if self.weaponsCommandLinkButton.isChecked():
			toggles += 'weapons,'
		if self.toolsCommandLinkButton.isChecked():
			toggles += 'tools,'
		if self.cratesCommandLinkButton.isChecked():
			toggles += 'crates'
		if toggles != '':
			if toggles[len(toggles)-1] == ',':
				toggles = toggles[:len(toggles)-1]

		self.settings.set_option('Settings', 'ui_log_entry_toggles', toggles)
		self.LogEntriesDialog.close()
	
	def populateDetails(self):
		toggles = self.settings.get_option('Settings', 'ui_log_entry_toggles').split(',')
		
		if 'system' in toggles:
			self.systemCommandLinkButton.setChecked(True)
		if 'hats' in toggles:
			self.hatsCommandLinkButton.setChecked(True)
		if 'weapons' in toggles:
			self.weaponsCommandLinkButton.setChecked(True)
		if 'tools' in toggles:
			self.toolsCommandLinkButton.setChecked(True)
		if 'crates' in toggles:
			self.cratesCommandLinkButton.setChecked(True)