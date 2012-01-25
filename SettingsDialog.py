import Config, os
from PyQt4 import QtCore, QtGui

backpackViewerDict = {'0': 'OPTF2', '1': 'Steam', '2': 'TF2B', '3': 'TF2Items'}

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

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
		self.SettingsDialog.resize(530, 458)
		self.SettingsDialog.setWindowTitle('TF2Idle Settings')
		self.SettingsDialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/settings.png')))

		self.gridLayout = QtGui.QGridLayout(self.SettingsDialog)

		# Add tab widget and tabs
		self.tabWidget = QtGui.QTabWidget(self.SettingsDialog)
		self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

		self.generalTab = QtGui.QWidget()
		self.tf2idleTab = QtGui.QWidget()
		self.droplogTab = QtGui.QWidget()
		
		self.tabWidget.addTab(self.generalTab, 'General')
		self.tabWidget.addTab(self.tf2idleTab, 'TF2Idle')
		self.tabWidget.addTab(self.droplogTab, 'Drop Log')
		
		# Add layouts for tabs
		self.generalVBoxLayout = QtGui.QVBoxLayout(self.generalTab)
		self.tf2idleVBoxLayout = QtGui.QGridLayout(self.tf2idleTab)
		self.droplogVBoxLayout = QtGui.QGridLayout(self.droplogTab)
		
		# Create title style for section labels
		titleStyle = "QGroupBox {font-weight: bold;}"
		
		# General settings tab
		
		# Locations section
		self.locationsQGroupBox = QtGui.QGroupBox(self.generalTab)
		self.locationsQGroupBox.setStyleSheet(titleStyle)
		self.locationsQGroupBox.setTitle('Locations')
		
		self.generalVBoxLayout.addWidget(self.locationsQGroupBox)
		
		self.locationsGroupBoxLayout = QtGui.QGridLayout(self.locationsQGroupBox)
		
		self.steamLocationLabel = QtGui.QLabel(self.locationsQGroupBox)
		self.steamLocationLabel.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.steamLocationLabel.setText('Steam installation location:')
		self.locationsGroupBoxLayout.addWidget(self.steamLocationLabel, 0, 0, 1, 1)
		
		self.steamLocationLineEdit = QtGui.QLineEdit()
		self.steamLocationLineEdit.setFrame(True)
		self.steamLocationLineEdit.setToolTip('The path to your Steam installation. This folder should contain Steam.exe')
		self.locationsGroupBoxLayout.addWidget(self.steamLocationLineEdit, 0, 1, 1, 1)

		self.steamLocationButton = QtGui.QPushButton()
		self.steamLocationButton.setText('..')
		self.steamLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.steamLocationButton, 0, 2, 1, 1)
		
		self.secondarySteamappsLocationLabel = QtGui.QLabel(self.locationsQGroupBox)
		self.secondarySteamappsLocationLabel.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the TF2 GCFs. Optional, only if you wish to use sandboxes')
		self.secondarySteamappsLocationLabel.setText('Secondary Steamapps folder location:')
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationLabel, 1, 0, 1, 1)
		
		self.secondarySteamappsLocationLineEdit = QtGui.QLineEdit()
		self.secondarySteamappsLocationLineEdit.setFrame(True)
		self.secondarySteamappsLocationLineEdit.setToolTip('The path to your backup copy of the steamapps folder. This folder should contain the TF2 GCFs. Optional, only if you wish to use sandboxes')
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationLineEdit, 1, 1, 1, 1)
		
		self.secondarySteamappsLocationButton = QtGui.QPushButton()
		self.secondarySteamappsLocationButton.setText('..')
		self.secondarySteamappsLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.secondarySteamappsLocationButton, 1, 2, 1, 1)
		
		self.sandboxieLocationLabel = QtGui.QLabel(self.locationsQGroupBox)
		self.sandboxieLocationLabel.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.sandboxieLocationLabel.setText('Sandboxie installation location:')
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationLabel, 2, 0, 1, 1)
		
		self.sandboxieLocationLineEdit = QtGui.QLineEdit()
		self.sandboxieLocationLineEdit.setFrame(True)
		self.sandboxieLocationLineEdit.setToolTip('The path to your Sandboxie installation. This folder should contain sandboxie.exe. Optional, only if you wish to use sandboxes')
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationLineEdit, 2, 1, 1, 1)
		
		self.sandboxieLocationButton = QtGui.QPushButton()
		self.sandboxieLocationButton.setText('..')
		self.sandboxieLocationButton.setMaximumSize(QtCore.QSize(30, 20))
		self.locationsGroupBoxLayout.addWidget(self.sandboxieLocationButton, 2, 2, 1, 1)
		
		# Steam API section
		self.steamAPIGroupBox = QtGui.QGroupBox(self.generalTab)
		self.steamAPIGroupBox.setStyleSheet(titleStyle)
		self.steamAPIGroupBox.setTitle('Steam API Settings')
		
		self.generalVBoxLayout.addWidget(self.steamAPIGroupBox)

		self.SteamAPIGroupBoxLayout = QtGui.QGridLayout(self.steamAPIGroupBox)
		
		self.steamAPIKeyLabel = QtGui.QLabel(self.steamAPIGroupBox)
		self.steamAPIKeyLabel.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.steamAPIKeyLabel.setText('Steam API key:')
		self.SteamAPIGroupBoxLayout.addWidget(self.steamAPIKeyLabel, 0, 0, 1, 1)
		
		self.steamAPIKeyLineEdit = QtGui.QLineEdit()
		self.steamAPIKeyLineEdit.setFrame(True)
		self.steamAPIKeyLineEdit.setToolTip('Your Steam WebAPI key. Optional, only if you wish to use the drop log feature')
		self.SteamAPIGroupBoxLayout.addWidget(self.steamAPIKeyLineEdit, 0, 1, 1, 1)
		
		# Backpack viewer section
		self.backpackGroupBox = QtGui.QGroupBox(self.generalTab)
		self.backpackGroupBox.setStyleSheet(titleStyle)
		self.backpackGroupBox.setTitle('Backpack Viewer Settings')

		self.generalVBoxLayout.addWidget(self.backpackGroupBox)

		self.backpackGroupBoxLayout = QtGui.QGridLayout(self.backpackGroupBox)
		
		self.backpackViewerLabel = QtGui.QLabel(self.backpackGroupBox)
		self.backpackViewerLabel.setToolTip('Your choice of backpack viewer')
		self.backpackViewerLabel.setText('Backpack viewer:')
		self.backpackGroupBoxLayout.addWidget(self.backpackViewerLabel, 0, 0, 1, 1)
		
		self.backpackViewerComboBox = QtGui.QComboBox()
		self.backpackViewerComboBox.insertItem(1, 'OPTF2')
		self.backpackViewerComboBox.insertItem(2, 'Steam')
		self.backpackViewerComboBox.insertItem(3, 'TF2B')
		self.backpackViewerComboBox.insertItem(4, 'TF2Items')
		self.backpackGroupBoxLayout.addWidget(self.backpackViewerComboBox, 0, 1, 1, 1)
		
		# TF2 settings section
		self.TF2SettingsGroupBox = QtGui.QGroupBox(self.generalTab)
		self.TF2SettingsGroupBox.setStyleSheet(titleStyle)
		self.TF2SettingsGroupBox.setTitle('TF2 Settings')

		self.generalVBoxLayout.addWidget(self.TF2SettingsGroupBox)

		self.TF2SettingsGroupBoxLayout = QtGui.QGridLayout(self.TF2SettingsGroupBox)
		
		self.idleLaunchLabel = QtGui.QLabel(self.TF2SettingsGroupBox)
		self.idleLaunchLabel.setToolTip('Your TF2 launch options for idling')
		self.idleLaunchLabel.setText('Idle launch settings:')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchLabel, 0, 0, 1, 1)
		
		self.idleLaunchTextEdit = QtGui.QTextEdit()
		self.idleLaunchTextEdit.setTabChangesFocus(True)
		self.idleLaunchTextEdit.setToolTip('Your TF2 launch options for idling')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchTextEdit, 0, 1, 1, 1)
		
		self.idleLaunchTextButton = QtGui.QPushButton()
		self.idleLaunchTextButton.setText('Restore default launch settings')
		self.TF2SettingsGroupBoxLayout.addWidget(self.idleLaunchTextButton, 9, 1, 1, 1)
		
		# TF2Idle settings tab
		
		# Mode section
		self.sandboxesGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.sandboxesGroupBox.setStyleSheet(titleStyle)
		self.sandboxesGroupBox.setTitle('Sandboxes')

		self.tf2idleVBoxLayout.addWidget(self.sandboxesGroupBox)

		self.sandboxesGroupBoxLayout = QtGui.QGridLayout(self.sandboxesGroupBox)
		
		self.sandboxModeLabel = QtGui.QLabel(self.sandboxesGroupBox)
		self.sandboxModeLabel.setToolTip('Choose a Sandboxie mode')
		self.sandboxModeLabel.setText('Sandboxie mode:')
		self.sandboxesGroupBoxLayout.addWidget(self.sandboxModeLabel, 0, 0, 1, 1)

		self.hLayout = QtGui.QVBoxLayout()
		self.hLayout.setMargin(0)
		self.sandboxesGroupBoxLayout.addLayout(self.hLayout, 0, 1, 1, 1)
		
		self.easySandboxModeRadioButton = QtGui.QRadioButton()
		self.easySandboxModeRadioButton.setText('Easy sandbox mode (experimental)')
		self.hLayout.addWidget(self.easySandboxModeRadioButton)
		
		self.advancedSandboxModeRadioButton = QtGui.QRadioButton()
		self.advancedSandboxModeRadioButton.setText('Advanced sandbox mode')
		self.hLayout.addWidget(self.advancedSandboxModeRadioButton)
		
		self.sandboxModeDescriptionLabel = QtGui.QLabel(self.sandboxesGroupBox)
		self.sandboxModeDescriptionLabel.setToolTip('Sandbox mode description')
		italicfont = QtGui.QFont()
		italicfont.setItalic(True)
		self.sandboxModeDescriptionLabel.setFont(italicfont)
		self.sandboxModeDescriptionLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
		self.sandboxesGroupBoxLayout.addWidget(self.sandboxModeDescriptionLabel, 1, 1, 1, 1)
		
		# UI settings section
		self.userInterfaceSettingsGroupBox = QtGui.QGroupBox(self.tf2idleTab)
		self.userInterfaceSettingsGroupBox.setStyleSheet(titleStyle)
		self.userInterfaceSettingsGroupBox.setTitle('User Interface')

		self.tf2idleVBoxLayout.addWidget(self.userInterfaceSettingsGroupBox)

		self.userInterfaceSettingsGroupBoxLayout = QtGui.QGridLayout(self.userInterfaceSettingsGroupBox)
		
		self.noOfColumnsLabel = QtGui.QLabel()
		self.noOfColumnsLabel.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsLabel.setText('No of account boxes per row:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsLabel, 0, 0, 1, 1)
		
		self.noOfColumnsSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.noOfColumnsSlider.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsSlider.setTickInterval(1)
		self.noOfColumnsSlider.setMinimum(1)
		self.noOfColumnsSlider.setMaximum(5)
		self.noOfColumnsSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='no_of_columns'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsSlider, 0, 1, 1, 1)
		
		self.noOfColumnsSpinBox = QtGui.QSpinBox()
		self.noOfColumnsSpinBox.setToolTip('The number of account boxes to display per row')
		self.noOfColumnsSpinBox.setMinimum(1)
		self.noOfColumnsSpinBox.setMaximum(5)
		self.noOfColumnsSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='no_of_columns'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.noOfColumnsSpinBox, 0, 2, 1, 1)
		
		self.accountFontSizeLabel = QtGui.QLabel()
		self.accountFontSizeLabel.setToolTip('The size of the font used in the account boxes')
		self.accountFontSizeLabel.setText('Account box font size:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeLabel, 1, 0, 1, 1)
		
		self.accountFontSizeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.accountFontSizeSlider.setToolTip('The size of the icon used in the account boxes')
		self.accountFontSizeSlider.setTickInterval(1)
		self.accountFontSizeSlider.setMinimum(1)
		self.accountFontSizeSlider.setMaximum(50)
		self.accountFontSizeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='account_font_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeSlider, 1, 1, 1, 1)
		
		self.accountFontSizeSpinBox = QtGui.QSpinBox()
		self.accountFontSizeSpinBox.setToolTip('The size of the font used in the account boxes')
		self.accountFontSizeSpinBox.setMinimum(1)
		self.accountFontSizeSpinBox.setMaximum(50)
		self.accountFontSizeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='account_font_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountFontSizeSpinBox, 1, 2, 1, 1)
		
		self.accountIconSizeLabel = QtGui.QLabel()
		self.accountIconSizeLabel.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeLabel.setText('Account box icon size:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeLabel, 2, 0, 1, 1)
		
		self.accountIconSizeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, )
		self.accountIconSizeSlider.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeSlider.setTickInterval(1)
		self.accountIconSizeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='account_icon_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeSlider, 2, 1, 1, 1)
		
		self.accountIconSizeSpinBox = QtGui.QSpinBox()
		self.accountIconSizeSpinBox.setToolTip('The size of the icon used in the account boxes')
		self.accountIconSizeSpinBox.setMinimum(0)
		self.accountIconSizeSpinBox.setMaximum(99)
		self.accountIconSizeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='account_icon_size'))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconSizeSpinBox, 2, 2, 1, 1)
		
		self.accountIconLabel = QtGui.QLabel()
		self.accountIconLabel.setToolTip('Choose an image to use as the account box icons')
		self.accountIconLabel.setText('Account box icon:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconLabel, 3, 0, 1, 1)
		
		self.accountIconLineEdit = QtGui.QLineEdit()
		self.accountIconLineEdit.setFrame(True)
		self.accountIconLineEdit.setToolTip('Choose an image to use as the account box icons')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconLineEdit, 3, 1, 1, 1)

		self.accountIconButton = QtGui.QPushButton()
		self.accountIconButton.setText('..')
		self.accountIconButton.setMaximumSize(QtCore.QSize(30, 20))
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconButton, 3, 2, 1, 1)
		
		self.accountIconRestoreButton = QtGui.QPushButton()
		self.accountIconRestoreButton.setText('Restore default icon')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountIconRestoreButton, 4, 1, 1, 1)
		
		self.accountBoxPreviewLabel = QtGui.QLabel()
		self.accountBoxPreviewLabel.setToolTip('Account box preview')
		self.accountBoxPreviewLabel.setText('Account box preview:')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.accountBoxPreviewLabel, 5, 0, 1, 1)

		ui_account_box_font_size = self.settings.get_option('Settings', 'ui_account_box_font_size')
		ui_account_box_icon_size = int(self.settings.get_option('Settings', 'ui_account_box_icon_size'))
		ui_account_box_icon = self.settings.get_option('Settings', 'ui_account_box_icon')

		self.commandLinkButton = QtGui.QCommandLinkButton()
		icon = QtGui.QIcon()
		if ui_account_box_icon != '':
			icon.addPixmap(QtGui.QPixmap(ui_account_box_icon))
		else:
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
			icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.commandLinkButton.setIcon(icon)
		self.commandLinkButton.setIconSize(QtCore.QSize(ui_account_box_icon_size, ui_account_box_icon_size))
		self.commandLinkButton.setCheckable(True)
		self.commandLinkButton.setStyleSheet('font: %spt "TF2 Build";' % ui_account_box_font_size)
		self.commandLinkButton.setText('Idling account')
		self.userInterfaceSettingsGroupBoxLayout.addWidget(self.commandLinkButton, 6, 1, 1, 1)
		
		# Drop log settings tab

		# Poll time section
		self.dropLogGroupBox = QtGui.QGroupBox(self.droplogTab)
		self.dropLogGroupBox.setStyleSheet(titleStyle)
		self.dropLogGroupBox.setTitle('Drop Log')

		self.droplogVBoxLayout.addWidget(self.dropLogGroupBox)

		self.dropLogGroupBoxLayout = QtGui.QGridLayout(self.dropLogGroupBox)
		
		self.pollTimeLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.pollTimeLabel.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeLabel.setText('Backpack polling interval (mins):')
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeLabel, 0, 0, 1, 1)

		self.pollTimeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.pollTimeSlider.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeSlider.setTickInterval(1)
		self.pollTimeSlider.setMinimum(1)
		self.pollTimeSlider.setMaximum(30)
		self.pollTimeSlider.valueChanged[int].connect(curry(self.changeValue, spinbox='log_poll_time'))
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeSlider, 0, 1, 1, 1)
		
		self.pollTimeSpinBox = QtGui.QSpinBox()
		self.pollTimeSpinBox.setToolTip('Choose the amount of time between backpack polls')
		self.pollTimeSpinBox.setMinimum(1)
		self.pollTimeSpinBox.setMaximum(30)
		self.pollTimeSpinBox.valueChanged[int].connect(curry(self.changeSlider, slider='log_poll_time'))
		self.dropLogGroupBoxLayout.addWidget(self.pollTimeSpinBox, 0, 2, 1, 1)
		
		# Drop log UI section
		self.dropLogUIGroupBox = QtGui.QGroupBox(self.droplogTab)
		self.dropLogUIGroupBox.setStyleSheet(titleStyle)
		self.dropLogUIGroupBox.setTitle('User Interface')

		self.droplogVBoxLayout.addWidget(self.dropLogUIGroupBox)

		self.dropLogUIGroupBoxLayout = QtGui.QGridLayout(self.dropLogUIGroupBox)
		
		self.dropLogBackgroundColourLabel = QtGui.QLabel(self.dropLogGroupBox)
		self.dropLogBackgroundColourLabel.setToolTip('The background colour used in the log viewer')
		self.dropLogBackgroundColourLabel.setText('Drop log background colour:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourLabel, 0, 0, 1, 1)

		self.dropLogBackgroundColourFrame = QtGui.QLineEdit()
		self.dropLogBackgroundColourFrame.setReadOnly(True)
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourFrame, 0, 1, 1, 1)

		self.dropLogBackgroundColourButton = QtGui.QPushButton()
		self.dropLogBackgroundColourButton.setText('..')
		self.dropLogBackgroundColourButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogBackgroundColourButton, 0, 2, 1, 1)
		
		self.dropLogFontColourLabel = QtGui.QLabel(self.dropLogUIGroupBox)
		self.dropLogFontColourLabel.setToolTip('The font colour used in the log viewer')
		self.dropLogFontColourLabel.setText('Drop log font colour:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourLabel, 1, 0, 1, 1)

		self.dropLogFontColourFrame = QtGui.QLineEdit()
		self.dropLogFontColourFrame.setReadOnly(True)
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourFrame, 1, 1, 1, 1)

		self.dropLogFontColourButton = QtGui.QPushButton()
		self.dropLogFontColourButton.setText('..')
		self.dropLogFontColourButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontColourButton, 1, 2, 1, 1)
		
		self.dropLogFontLabel = QtGui.QLabel(self.dropLogUIGroupBox)
		self.dropLogFontLabel.setToolTip('The font used in the log viewer')
		self.dropLogFontLabel.setText('Drop log font:')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontLabel, 2, 0, 1, 1)
		
		self.dropLogFontPreviewLabel = QtGui.QLabel()
		self.dropLogFontPreviewLabel.setText('You have found: Razorback!')
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontPreviewLabel, 2, 1, 1, 1)
		
		self.dropLogFontButton = QtGui.QPushButton()
		self.dropLogFontButton.setText('..')
		self.dropLogFontButton.setMaximumSize(QtCore.QSize(30, 20))
		self.dropLogUIGroupBoxLayout.addWidget(self.dropLogFontButton, 2, 2, 1, 1)

		# Add buttons
		self.buttonBox = QtGui.QDialogButtonBox(self.SettingsDialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

		# Set mininmum label lengths on all tabs to align right hand side widgets
		self.setMinLabelLength(self.generalTab)
		self.setMinLabelLength(self.tf2idleTab)
		self.setMinLabelLength(self.droplogTab)
		
		# Signal connections
		QtCore.QObject.connect(self.steamLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='steam_location'))
		QtCore.QObject.connect(self.secondarySteamappsLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='secondary_steamapps_location'))
		QtCore.QObject.connect(self.sandboxieLocationButton, QtCore.SIGNAL('clicked()'), curry(self.getDirectory, action='sandboxie_location'))
		QtCore.QObject.connect(self.idleLaunchTextButton, QtCore.SIGNAL('clicked()'), curry(self.restoreDefault, action='idle_launch'))
		QtCore.QObject.connect(self.easySandboxModeRadioButton, QtCore.SIGNAL('clicked()'), self.updateSandboxModeDescription)
		QtCore.QObject.connect(self.advancedSandboxModeRadioButton, QtCore.SIGNAL('clicked()'), self.updateSandboxModeDescription)
		QtCore.QObject.connect(self.accountIconButton, QtCore.SIGNAL('clicked()'), self.getIconFile)
		QtCore.QObject.connect(self.accountIconRestoreButton, QtCore.SIGNAL('clicked()'), curry(self.restoreDefault, action='account_icon'))
		QtCore.QObject.connect(self.dropLogBackgroundColourButton, QtCore.SIGNAL('clicked()'), curry(self.getColour, component='background'))
		QtCore.QObject.connect(self.dropLogFontColourButton, QtCore.SIGNAL('clicked()'), curry(self.getColour, component='font'))
		QtCore.QObject.connect(self.dropLogFontButton, QtCore.SIGNAL('clicked()'), self.getFont)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), SettingsDialog.reject)
		QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

		self.populateDetails()

	def setMinLabelLength(self, tabwidget):
		groupboxes = tabwidget.findChildren(QtGui.QGroupBox)
		labels = []
		for groupbox in groupboxes:
			labels.extend(groupbox.findChildren(QtGui.QLabel))
		largestwidth = labels[0].sizeHint().width()
		for label in labels[1:]:
			if label.sizeHint().width() > largestwidth:
				largestwidth = label.sizeHint().width()
		for label in labels:
			label.setMinimumSize(QtCore.QSize(largestwidth, 0))

	def updatePreview(self, action, value):
		if action == 'account_font_size':
			self.commandLinkButton.setStyleSheet('font: %spt "TF2 Build";' % value)
		elif action == 'account_icon_size':
			self.commandLinkButton.setIconSize(QtCore.QSize(int(value), int(value)))
		elif action == 'account_icon':
			icon = QtGui.QIcon()
			if value != '':
				icon.addPixmap(QtGui.QPixmap(value))
			else:
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.Off)
				icon.addPixmap(QtGui.QPixmap(returnResourcePath('images/selected_button.png')), QtGui.QIcon.Selected, QtGui.QIcon.On)
			self.commandLinkButton.setIcon(icon)

	def updateSandboxModeDescription(self):
		if self.easySandboxModeRadioButton.isChecked():
			self.sandboxModeDescriptionLabel.setText('TF2Idle will create and delete sandboxes\non the fly as needed')
		else:
			self.sandboxModeDescriptionLabel.setText('You will need to create sandboxes for the\naccounts yourself')

	def changeValue(self, value, spinbox):
		if spinbox == 'no_of_columns':
			self.noOfColumnsSpinBox.setValue(int(value))
		elif spinbox == 'account_font_size':
			self.accountFontSizeSpinBox.setValue(int(value))
			self.updatePreview('account_font_size', value)
		elif spinbox == 'account_icon_size':
			self.accountIconSizeSpinBox.setValue(int(value))
			self.updatePreview('account_icon_size', value)
		elif spinbox == 'log_poll_time':
			self.pollTimeSpinBox.setValue(int(value))

	def changeSlider(self, value, slider):
		if slider == 'no_of_columns':
			self.noOfColumnsSlider.setValue(int(value))
		if slider == 'account_font_size':
			self.accountFontSizeSlider.setValue(int(value))
		elif slider == 'account_icon_size':
			self.accountIconSizeSlider.setValue(int(value))
		elif slider == 'log_poll_time':
			self.pollTimeSlider.setValue(int(value))
	
	def getDirectory(self, action):
		if action == 'steam_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Steam Directory'))
			if filepath:
				self.steamLocationLineEdit.setText(filepath)
		elif action == 'secondary_steamapps_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Secondary Steamapps Directory'))
			if filepath:
				self.secondarySteamappsLocationLineEdit.setText(filepath)
		elif action == 'sandboxie_location':
			filepath = str(QtGui.QFileDialog.getExistingDirectory(self.generalTab, 'Select Sandboxie Directory'))
			if filepath:
				self.sandboxieLocationLineEdit.setText(filepath)
	
	def getIconFile(self):
		filepath = str(QtGui.QFileDialog.getOpenFileName(self.tf2idleTab, 'Select Account Icon', filter='Images (*.png *.jpeg *.jpg *.gif *.bmp)'))
		if filepath:
			self.accountIconLineEdit.setText(filepath)
			self.updatePreview('account_icon', filepath)

	def getColour(self, component):
		colour = QtGui.QColorDialog.getColor()
		if colour.isValid():
			if component == 'background':
				self.dropLogBackgroundColourFrame.setStyleSheet('background-color: %s;' % colour.name())
				self.dropLogBackgroundColour = str(colour.name())[1:]
			elif component == 'font':
				self.dropLogFontColourFrame.setStyleSheet('background-color: %s;' % colour.name())
				self.dropLogFontColour = str(colour.name())[1:]
	
	def getFont(self):
		font, valid = QtGui.QFontDialog().getFont(self.dropLogFont)
		if valid:
			self.dropLogFont = font
			self.dropLogFontPreviewLabel.setFont(font)
			self.dropLogFontSize = font.pointSize()
			self.dropLogFontFamily = font.family()
			self.dropLogFontItalic = font.style()
			self.dropLogFontBold = font.weight()

	def restoreDefault(self, action):
		if action == 'idle_launch':
			self.idleLaunchTextEdit.setText('+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
		elif action == 'account_icon':
			self.accountIconLineEdit.setText('')
			self.updatePreview('account_icon', '')
	
	def accept(self):
		steam_location = str(self.steamLocationLineEdit.text())
		secondary_steamapps_location = str(self.secondarySteamappsLocationLineEdit.text())
		sandboxie_location = str(self.sandboxieLocationLineEdit.text())
		API_key = str(self.steamAPIKeyLineEdit.text()).strip()
		backpack_viewer = backpackViewerDict[str(self.backpackViewerComboBox.currentIndex())]
		launch_options = str(self.idleLaunchTextEdit.toPlainText())
		ui_no_of_columns = str(self.noOfColumnsSpinBox.text())
		ui_account_box_font_size = str(self.accountFontSizeSpinBox.text())
		ui_account_box_icon_size = str(self.accountIconSizeSpinBox.text())
		ui_account_box_icon = str(self.accountIconLineEdit.text())
		if self.easySandboxModeRadioButton.isChecked():
			easy_sandbox_mode = 'yes'
		elif self.advancedSandboxModeRadioButton.isChecked():
			easy_sandbox_mode = 'no'
		log_poll_time = str(self.pollTimeSpinBox.text())
		
		allowedFileTypes = ['.png', '.jpeg', '.jpg', '.gif', '.bmp']
		
		if steam_location == '':
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Please enter a Steam install location')
		elif launch_options == '':
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Please enter some launch options')
		elif ui_account_box_icon != '' and (not os.path.isfile(ui_account_box_icon) or os.path.splitext(ui_account_box_icon)[1] not in allowedFileTypes):
			QtGui.QMessageBox.warning(self.SettingsDialog, 'Error', 'Account icon is not a valid image file')
		else:
			self.settings.set_option('Settings', 'steam_location', steam_location)
			self.settings.set_option('Settings', 'secondary_steamapps_location', secondary_steamapps_location)
			self.settings.set_option('Settings', 'sandboxie_location', sandboxie_location)
			self.settings.set_option('Settings', 'API_key', API_key)
			self.settings.set_option('Settings', 'backpack_viewer', backpack_viewer)
			self.settings.set_option('Settings', 'launch_options', launch_options)
			self.settings.set_option('Settings', 'ui_no_of_columns', ui_no_of_columns)
			self.settings.set_option('Settings', 'ui_account_box_font_size', ui_account_box_font_size)
			self.settings.set_option('Settings', 'ui_account_box_icon_size', ui_account_box_icon_size)
			self.settings.set_option('Settings', 'ui_account_box_icon', ui_account_box_icon)
			self.settings.set_option('Settings', 'easy_sandbox_mode', easy_sandbox_mode)
			self.settings.set_option('Settings', 'log_poll_time', log_poll_time)
			self.settings.set_option('Settings', 'ui_log_background_colour', self.dropLogBackgroundColour)
			self.settings.set_option('Settings', 'ui_log_font_colour', self.dropLogFontColour)
			self.settings.set_option('Settings', 'ui_log_font_size', str(self.dropLogFontSize))
			self.settings.set_option('Settings', 'ui_log_font_family', str(self.dropLogFontFamily))
			self.settings.set_option('Settings', 'ui_log_font_style', str(self.dropLogFontItalic))
			self.settings.set_option('Settings', 'ui_log_font_weight', str(self.dropLogFontBold))

			self.SettingsDialog.close()
		
	def populateDetails(self):
		self.steamLocationLineEdit.setText(self.settings.get_option('Settings', 'steam_location'))
		self.secondarySteamappsLocationLineEdit.setText(self.settings.get_option('Settings', 'secondary_steamapps_location'))
		self.sandboxieLocationLineEdit.setText(self.settings.get_option('Settings', 'sandboxie_location'))
		self.steamAPIKeyLineEdit.setText(self.settings.get_option('Settings', 'API_key'))
		viewer = [key for key, value in backpackViewerDict.iteritems() if value == self.settings.get_option('Settings', 'backpack_viewer')][0]
		self.backpackViewerComboBox.setCurrentIndex(int(viewer))
		self.idleLaunchTextEdit.setText(self.settings.get_option('Settings', 'launch_options'))
		self.noOfColumnsSpinBox.setValue(int(self.settings.get_option('Settings', 'ui_no_of_columns')))
		self.accountFontSizeSpinBox.setValue(int(self.settings.get_option('Settings', 'ui_account_box_font_size')))
		self.accountIconSizeSlider.setValue(int(self.settings.get_option('Settings', 'ui_account_box_icon_size')))
		self.accountIconLineEdit.setText(self.settings.get_option('Settings', 'ui_account_box_icon'))
		if self.settings.get_option('Settings', 'easy_sandbox_mode') == 'yes':
			self.easySandboxModeRadioButton.setChecked(True)
		else:
			self.advancedSandboxModeRadioButton.setChecked(True)
		self.pollTimeSpinBox.setValue(int(self.settings.get_option('Settings', 'log_poll_time')))
		self.pollTimeSlider.setValue(int(self.settings.get_option('Settings', 'log_poll_time')))
		self.dropLogBackgroundColour = self.settings.get_option('Settings', 'ui_log_background_colour')
		self.dropLogBackgroundColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogBackgroundColour)

		self.dropLogFontColour = self.settings.get_option('Settings', 'ui_log_font_colour')
		self.dropLogFontColourFrame.setStyleSheet('background-color: #%s;' % self.dropLogFontColour)

		self.dropLogFontSize = self.settings.get_option('Settings', 'ui_log_font_size')
		self.dropLogFontFamily = self.settings.get_option('Settings', 'ui_log_font_family')
		self.dropLogFontItalic = self.settings.get_option('Settings', 'ui_log_font_style')
		self.dropLogFontBold = self.settings.get_option('Settings', 'ui_log_font_weight')
		self.dropLogFont = QtGui.QFont(self.dropLogFontFamily, int(self.dropLogFontSize), int(self.dropLogFontBold), self.dropLogFontItalic == '1')
		self.dropLogFontPreviewLabel.setFont(self.dropLogFont)
		
		self.updateSandboxModeDescription()