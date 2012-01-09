import Config
from PyQt4 import QtCore, QtGui

class Ui_SettingsDialog(object):
	def __init__(self, SettingsDialog):
		self.settings = Config.settings
		
		# Create dialog
		self.SettingsDialog = SettingsDialog
		self.SettingsDialog.setObjectName('SettingsDialog')
		self.SettingsDialog.setWindowModality(QtCore.Qt.NonModal)
		self.SettingsDialog.resize(450, 350)
		self.SettingsDialog.setMinimumSize(QtCore.QSize(450, 350))
		SettingsDialog.setWindowTitle('Settings')
		
		# Add layout widget
		self.gridLayoutWidget = QtGui.QWidget(SettingsDialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 381, 279))
		self.gridLayoutWidget.setObjectName('gridLayoutWidget')
		
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(0)
		self.gridLayout.setObjectName('gridLayout')
		
		# Set font for sections
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		
		# Steam account section
		self.label = QtGui.QLabel(self.gridLayoutWidget)
		self.label.setFont(font)
		self.label.setObjectName('label')
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		self.label.setText('TF2 Settings')
		
		self.label2 = QtGui.QLabel(self.gridLayoutWidget)
		self.label2.setObjectName('label2')
		self.label2.setToolTip('Launch settings')
		self.label2.setText('Launch settings:')
		self.gridLayout.addWidget(self.label2, 1, 0, 1, 1)
		
		self.lineEdit2 = QtGui.QLineEdit(self.gridLayoutWidget)
		self.lineEdit2.setFrame(True)
		self.lineEdit2.setObjectName('lineEdit2')
		self.gridLayout.addWidget(self.lineEdit2, 1, 1, 1, 1)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
		self.buttonBox.setGeometry(QtCore.QRect(60, 300, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.buttonBox.setObjectName('buttonBox')
		
		# Signal connections
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), SettingsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

		self.populateDetails()
	
	def accept(self):
		launch_options = str(self.lineEdit2.text())
		
		if launch_options == '':
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Please enter some launch options')
		else:
			self.settings.set_section('Settings')
			self.settings.set_option('launch_options', launch_options)
			self.SettingsDialog.close()
		
	def populateDetails(self):
		print self.settings.get_sections()
		self.settings.set_section('Settings')
		if self.settings.has_section('Settings'):
			self.lineEdit2.setText(self.settings.get_option('launch_options'))
		else:
			self.settings.add_section()
			self.lineEdit2.setText('+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')