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
		self.LogEntriesDialog.resize(220, 250)
		self.LogEntriesDialog.setMinimumSize(QtCore.QSize(self.LogEntriesDialog.width(), self.LogEntriesDialog.height()))
		self.LogEntriesDialog.setWindowTitle('Select log entries')
		self.LogEntriesDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/select_group.png')))
		
		# Add layout widget
		self.gridLayoutWidget = QtGui.QWidget(LogEntriesDialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(25, 10, self.LogEntriesDialog.width()-50, self.LogEntriesDialog.height()-40))
		
		self.gridLayout = QtGui.QVBoxLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(0)
		
		# Add checkboxes
		self.systemCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
		self.systemCheckBox.setText('System messages')
		self.gridLayout.addWidget(self.systemCheckBox)
		
		self.hatsCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
		self.hatsCheckBox.setText('Hat drops')
		self.gridLayout.addWidget(self.hatsCheckBox)
		
		self.weaponsCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
		self.weaponsCheckBox.setText('Weapon drops')
		self.gridLayout.addWidget(self.weaponsCheckBox)
		
		self.toolsCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
		self.toolsCheckBox.setText('Tool drops')
		self.gridLayout.addWidget(self.toolsCheckBox)
		
		self.cratesCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
		self.cratesCheckBox.setText('Crate drops')
		self.gridLayout.addWidget(self.cratesCheckBox)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self.gridLayoutWidget)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setCenterButtons(True)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.gridLayout.addWidget(self.buttonBox)
		
		# Signal connections
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), LogEntriesDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(self.LogEntriesDialog)

		self.populateDetails()
	
	def accept(self):
		self.settings.set_section('Settings')
		toggles = ''

		if self.systemCheckBox.isChecked():
			toggles += 'system,'
		if self.hatsCheckBox.isChecked():
			toggles += 'hats,'
		if self.weaponsCheckBox.isChecked():
			toggles += 'weapons,'
		if self.toolsCheckBox.isChecked():
			toggles += 'tools,'
		if self.cratesCheckBox.isChecked():
			toggles += 'crates'
		if toggles != '':
			if toggles[len(toggles)-1] == ',':
				toggles = toggles[:len(toggles)-1]

		self.settings.set_option('ui_log_entry_toggles', toggles)
		self.LogEntriesDialog.close()
	
	def populateDetails(self):
		self.settings.set_section('Settings')
		toggles = self.settings.get_option('ui_log_entry_toggles').split(',')
		
		if 'system' in toggles:
			self.systemCheckBox.setChecked(True)
		if 'hats' in toggles:
			self.hatsCheckBox.setChecked(True)
		if 'weapons' in toggles:
			self.weaponsCheckBox.setChecked(True)
		if 'tools' in toggles:
			self.toolsCheckBox.setChecked(True)
		if 'crates' in toggles:
			self.cratesCheckBox.setChecked(True)