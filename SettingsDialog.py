import Config, os
from PyQt4 import QtCore, QtGui

backpackViewerDict = {'0': 'OPTF2', '1': 'Steam', '2': 'TF2B', '3': 'TF2Items'}

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + 'images' + os.sep + resource
	else:
		return 'images' + os.sep + resource

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

class Ui_SettingsDialog(object):
	def __init__(self, SettingsDialog):
		self.settings = Config.settings
		
		# Create dialog
		self.SettingsDialog = SettingsDialog
		self.SettingsDialog.setWindowModality(QtCore.Qt.NonModal)
		self.SettingsDialog.resize(450, 400)
		self.SettingsDialog.setMinimumSize(QtCore.QSize(self.SettingsDialog.width(), self.SettingsDialog.height()))
		self.SettingsDialog.setWindowTitle('TF2Idle Settings')
		self.SettingsDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('settings.png')))

		# Add layout widget
		self.gridLayoutWidget = QtGui.QWidget(SettingsDialog)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, self.SettingsDialog.width()-50, self.SettingsDialog.height()-70))
		
		self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
		self.gridLayout.setMargin(0)
		
		# Set font for section labels
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		
		# Locations section
		self.locationsLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.locationsLabel.setFont(font)
		self.locationsLabel.setText('Locations')
		self.gridLayout.addWidget(self.locationsLabel, 0, 0, 1, 1)
		
		self.steamLocationLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamLocationLabel.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.steamLocationLabel.setText('Steam installation location:')
		self.gridLayout.addWidget(self.steamLocationLabel, 1, 0, 1, 1)
		
		self.steamLocationLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.steamLocationLineEdit.setFrame(True)
		self.steamLocationLineEdit.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.gridLayout.addWidget(self.steamLocationLineEdit, 1, 1, 1, 1)

		self.steamLocationButton = QtGui.QPushButton(self.gridLayoutWidget)
		self.steamLocationButton.setText('..')
		self.steamLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.gridLayout.addWidget(self.steamLocationButton, 1, 2, 1, 1)
		
		self.secondarySteamappsLocationLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.secondarySteamappsLocationLabel.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the TF2 GCFs. Optional, only if you wish to use sandboxes')
		self.secondarySteamappsLocationLabel.setText('Secondary Steamapps folder location:')
		self.gridLayout.addWidget(self.secondarySteamappsLocationLabel, 2, 0, 1, 1)
		
		self.secondarySteamappsLocationLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.secondarySteamappsLocationLineEdit.setFrame(True)
		self.secondarySteamappsLocationLineEdit.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the TF2 GCFs. Optional, only if you wish to use sandboxes')
		self.gridLayout.addWidget(self.secondarySteamappsLocationLineEdit, 2, 1, 1, 1)
		
		self.secondarySteamappsLocationButton = QtGui.QPushButton(self.gridLayoutWidget)
		self.secondarySteamappsLocationButton.setText('..')
		self.secondarySteamappsLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.gridLayout.addWidget(self.secondarySteamappsLocationButton, 2, 2, 1, 1)
		
		self.sandboxieLocationLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.sandboxieLocationLabel.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.sandboxieLocationLabel.setText('Sandboxie installation location:')
		self.gridLayout.addWidget(self.sandboxieLocationLabel, 3, 0, 1, 1)
		
		self.sandboxieLocationLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.sandboxieLocationLineEdit.setFrame(True)
		self.sandboxieLocationLineEdit.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.gridLayout.addWidget(self.sandboxieLocationLineEdit, 3, 1, 1, 1)
		
		self.sandboxieLocationButton = QtGui.QPushButton(self.gridLayoutWidget)
		self.sandboxieLocationButton.setText('..')
		self.sandboxieLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.gridLayout.addWidget(self.sandboxieLocationButton, 3, 2, 1, 1)
		
		# Steam API section
		self.SteamAPILabel = QtGui.QLabel(self.gridLayoutWidget)
		self.SteamAPILabel.setFont(font)
		self.SteamAPILabel.setText('Steam API Settings')
		self.gridLayout.addWidget(self.SteamAPILabel, 4, 0, 1, 1)
		
		self.steamAPIKeyLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.steamAPIKeyLabel.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.steamAPIKeyLabel.setText('Steam API key:')
		self.gridLayout.addWidget(self.steamAPIKeyLabel, 5, 0, 1, 1)
		
		self.steamAPIKeyLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
		self.steamAPIKeyLineEdit.setFrame(True)
		self.steamAPIKeyLineEdit.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.gridLayout.addWidget(self.steamAPIKeyLineEdit, 5, 1, 1, 1)
		
		# Backpack viewer section
		self.backpackLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.backpackLabel.setFont(font)
		self.backpackLabel.setText('Backpack Viewer Settings')
		self.gridLayout.addWidget(self.backpackLabel, 6, 0, 1, 1)
		
		self.backpackViewerLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.backpackViewerLabel.setToolTip('Your choice of backpack viewer')
		self.backpackViewerLabel.setText('Backpack viewer:')
		self.gridLayout.addWidget(self.backpackViewerLabel, 7, 0, 1, 1)
		
		self.backpackViewerComboBox = QtGui.QComboBox(self.gridLayoutWidget)
		self.backpackViewerComboBox.insertItem(1, 'OPTF2')
		self.backpackViewerComboBox.insertItem(2, 'Steam')
		self.backpackViewerComboBox.insertItem(3, 'TF2B')
		self.backpackViewerComboBox.insertItem(4, 'TF2Items')
		self.gridLayout.addWidget(self.backpackViewerComboBox, 7, 1, 1, 1)
		
		# TF2 settings section
		self.TF2SettingsLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.TF2SettingsLabel.setFont(font)
		self.TF2SettingsLabel.setText('TF2 Settings')
		self.gridLayout.addWidget(self.TF2SettingsLabel, 8, 0, 1, 1)
		
		self.idleLaunchLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.idleLaunchLabel.setToolTip('Your TF2 launch options for idling')
		self.idleLaunchLabel.setText('Idle launch settings:')
		self.gridLayout.addWidget(self.idleLaunchLabel, 9, 0, 1, 1)
		
		self.idleLaunchTextEdit = QtGui.QTextEdit(self.gridLayoutWidget)
		self.idleLaunchTextEdit.setTabChangesFocus(True)
		self.idleLaunchTextEdit.setToolTip('Your TF2 launch options for idling')
		self.gridLayout.addWidget(self.idleLaunchTextEdit, 9, 1, 1, 1)
		
		# TF2Idle settings section
		self.TF2IdleSettingsLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.TF2IdleSettingsLabel.setFont(font)
		self.TF2IdleSettingsLabel.setText('TF2Idle Settings')
		self.gridLayout.addWidget(self.TF2IdleSettingsLabel, 10, 0, 1, 1)
		
		self.noOfColumnsLabel = QtGui.QLabel(self.gridLayoutWidget)
		self.noOfColumnsLabel.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsLabel.setText('No of account boxes per row:')
		self.gridLayout.addWidget(self.noOfColumnsLabel, 11, 0, 1, 1)
		
		self.noOfColumnsSpinBox = QtGui.QSpinBox(self.gridLayoutWidget)
		self.noOfColumnsSpinBox.setMinimum(1)
		self.noOfColumnsSpinBox.setMaximum(5)
		self.gridLayout.addWidget(self.noOfColumnsSpinBox, 11, 1, 1, 1)
		
		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
		self.buttonBox.setGeometry(QtCore.QRect(60, self.gridLayoutWidget.height() + 20, 340, 30))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		
		# Signal connections
		QtCore.QObject.connect(self.steamLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='steam_location'))
		QtCore.QObject.connect(self.secondarySteamappsLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='secondary_steamapps_location'))
		QtCore.QObject.connect(self.sandboxieLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='sandboxie_location'))
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), SettingsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

		self.populateDetails()
	
	def getDirectory(self, action):
		if action == 'steam_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.gridLayoutWidget, 'Select Steam Directory'))
			self.steamLocationLineEdit.setText(filepath)
		elif action == 'secondary_steamapps_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.gridLayoutWidget, 'Select Secondary Steamapps Directory'))
			self.secondarySteamappsLocationLineEdit.setText(filepath)
		else:
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.gridLayoutWidget, 'Select Sandboxie Directory'))
			self.sandboxieLocationLineEdit.setText(filepath)
	
	def accept(self):		
		steam_location = str(self.steamLocationLineEdit.text())
		secondary_steamapps_location = str(self.secondarySteamappsLocationLineEdit.text())
		sandboxie_location = str(self.sandboxieLocationLineEdit.text())
		API_key = str(self.steamAPIKeyLineEdit.text())
		backpack_viewer = backpackViewerDict[str(self.backpackViewerComboBox.currentIndex())]
		launch_options = str(self.idleLaunchTextEdit.toPlainText())
		ui_no_of_columns = str(self.noOfColumnsSpinBox.text())
		
		if steam_location == '':
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Please enter a Steam install location')
		elif launch_options == '':
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Please enter some launch options')
		else:
			self.settings.set_section('Settings')
			self.settings.set_option('steam_location', steam_location)
			self.settings.set_option('secondary_steamapps_location', secondary_steamapps_location)
			self.settings.set_option('sandboxie_location', sandboxie_location)
			self.settings.set_option('API_key', API_key)
			self.settings.set_option('backpack_viewer', backpack_viewer)
			self.settings.set_option('launch_options', launch_options)
			self.settings.set_option('ui_no_of_columns', ui_no_of_columns)
			self.SettingsDialog.close()
		
	def populateDetails(self):
		self.settings.set_section('Settings')
		self.steamLocationLineEdit.setText(self.settings.get_option('steam_location'))
		self.secondarySteamappsLocationLineEdit.setText(self.settings.get_option('secondary_steamapps_location'))
		self.sandboxieLocationLineEdit.setText(self.settings.get_option('sandboxie_location'))
		self.steamAPIKeyLineEdit.setText(self.settings.get_option('API_key'))
		viewer = [key for key, value in backpackViewerDict.iteritems() if value == self.settings.get_option('backpack_viewer')][0]
		self.backpackViewerComboBox.setCurrentIndex(int(viewer))
		self.idleLaunchTextEdit.setText(self.settings.get_option('launch_options'))
		self.noOfColumnsSpinBox.setValue(int(self.settings.get_option('ui_no_of_columns')))