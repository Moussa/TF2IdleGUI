import Config, os, urllib2, webbrowser
import Sandboxie
import Version
from PyQt4 import QtCore, QtGui
from sets import Set
from SettingsDialog import Ui_SettingsDialog
from DropLogView import DropLogView
from AccountsView import AccountsView

def returnResourcePath(resource):
	MEIPASS2 = '_MEIPASS2'
	if MEIPASS2 in os.environ:
		return os.environ[MEIPASS2] + resource
	else:
		return resource

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.settings = Config.settings
		self.toolBars = []
		self.sandboxieINIIsModified = False

		self.setWindowTitle('TF2Idle')
		windowXSize, windowYSize = eval(self.settings.get_option('Settings', 'ui_window_size'))
		self.resize(windowXSize, windowYSize)
		self.setWindowIcon(QtGui.QIcon(returnResourcePath('images/tf2idle.png')))
		
		self.drawToolBars()
		
		# Add menu bar
		self.menuBar = QtGui.QMenuBar(self)
		self.menuBar.setObjectName('menubar')
		self.setMenuBar(self.menuBar)
		
		# Add File menu
		fileMenu = self.addMenu('File')
		self.addSubMenu(fileMenu, text='Settings', shortcut='Ctrl+S', action={'trigger':'triggered()', 'action':self.openSettings})
		fileMenu.addSeparator()
		self.addSubMenu(fileMenu, text='Exit', shortcut='Ctrl+Q', action={'trigger':'triggered()', 'action':self.close})

		# Add About menu
		helpMenu = self.addMenu('Help')
		self.addSubMenu(helpMenu, text='Readme / Source', action={'trigger':'triggered()', 'action':self.openGithub})
		self.addSubMenu(helpMenu, text='Steam group', action={'trigger':'triggered()', 'action':self.openSteamGroup})
		self.addSubMenu(helpMenu, text='Check for update', action={'trigger':'triggered()', 'action':self.checkForUpdate})
		self.addSubMenu(helpMenu, text='About', action={'trigger':'triggered()', 'action':self.showAbout})
		
		# Set starting view as accounts page
		self.accountsView = AccountsView(self)
		self.dropLogView = DropLogView(self)
		
		self.stackedWidget = QtGui.QStackedWidget(self)
		self.stackedWidget.addWidget(self.accountsView)
		self.stackedWidget.addWidget(self.dropLogView)
		self.setCentralWidget(self.stackedWidget)
		
		# Connect signals used for passing account information between views
		QtCore.QObject.connect(self.accountsView, QtCore.SIGNAL('returnedSelectedAccounts(PyQt_PyObject)'), self.dropLogView.setSelectedAccounts)
		QtCore.QObject.connect(self.dropLogView, QtCore.SIGNAL('retrieveSelectedAccounts'), self.accountsView.returnSelectedAccounts)
		
		self.changeView('accounts')
	
	# Override right click context menu to display nothing
	def createPopupMenu(self):
		pass

	def closeEvent(self, event):
		reply = QtGui.QMessageBox.question(self, 'Quit', 'Are you sure to quit?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			# Save main window size on exit
			self.settings.set_option('Settings', 'ui_window_size', '(%s, %s)' % (self.width(), self.height()))
			# If sandboxie.ini has been modified restore from backup copy
			if self.sandboxieINIIsModified:
				Sandboxie.restoreSandboxieINI()
		else:
			event.ignore()

	def drawToolBars(self, hideRightToolbar=False):
		for toolbar in self.toolBars:
			toolbar.close()
			del toolbar
		self.toolBars = []
	
		if not hideRightToolbar:
			# Create vertical toolbar
			self.vtoolBar = QtGui.QToolBar(self)
			self.vtoolBar.setObjectName('vtoolBar')
			self.vtoolBar.setIconSize(QtCore.QSize(40, 40))
			self.vtoolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
			self.vtoolBar.setMovable(False)
		
		# Create horizontal toolbar
		self.htoolBar = QtGui.QToolBar(self)
		self.htoolBar.setObjectName('htoolBar')
		self.htoolBar.setIconSize(QtCore.QSize(40, 40))
		self.htoolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		self.htoolBar.setMovable(False)
		
		# Add toolbars to toolbar list so can be deleted when MainWindow is refreshed
		self.toolBars.append(self.vtoolBar)
		self.toolBars.append(self.htoolBar)
		
		# Attach toolbars to MainWindow
		if not hideRightToolbar:
			self.addToolBar(QtCore.Qt.RightToolBarArea, self.vtoolBar)
			self.toolBars.append(self.vtoolBar)

		self.addToolBar(QtCore.Qt.BottomToolBarArea, self.htoolBar)
		self.toolBars.append(self.htoolBar)
	
	def changeView(self, view):
		if view == 'accounts':
			self.drawToolBars()
			self.accountsView.updateWindow()
			self.stackedWidget.setCurrentIndex(0)
		elif view == 'log':
			self.drawToolBars(hideRightToolbar=True)
			self.dropLogView.updateWindow()
			self.stackedWidget.setCurrentIndex(1)
	
	def sandboxieINIHasBeenModified(self):
		self.sandboxieINIIsModified = True

	def addMenu(self, menuname):
		self.menu = QtGui.QMenu(self.menuBar)
		self.menu.setObjectName('menu' + menuname)
		self.menu.setTitle(menuname)
		self.menuBar.addAction(self.menu.menuAction())
		return self.menu
	
	def addSubMenu(self, menu, shortcut=None, text=None, tooltip=None, action=None):
		self.action = QtGui.QAction(self)
		if shortcut:
			self.action.setShortcut(shortcut)
		menu.addAction(self.action)
		if action:
			QtCore.QObject.connect(self.action, QtCore.SIGNAL(action['trigger']), action['action'])
		if text:
			self.action.setText(text)
		if tooltip:
			self.action.setToolTip(tooltip)
	
	def openSettings(self):
		dialogWindow = SettingsDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.accountsView.updateAccountBoxes()
		self.dropLogView.updateLogDisplay()

	def openGithub(self):
		webbrowser.open('http://github.com/Moussekateer/TF2IdleGUI')

	def openSteamGroup(self):
		webbrowser.open('http://steamcommunity.com/groups/tf2idletool')

	def checkForUpdate(self):
		self.updateCheckThread = UpdateCheckThread()
		QtCore.QObject.connect(self.updateCheckThread, QtCore.SIGNAL('recievedVersion'), self.updateDialog)
		self.updateCheckThread.start()
	
	def updateDialog(self, currentversion):
		if currentversion is None:
			QtGui.QMessageBox.warning(self, 'Error', 'Could not retrieve the current version number, check your connection.')
		else:
			currentversionlist = currentversion.split('.')
			version = Version.version.split('.')
			update = False
			index = 0
			for n in currentversionlist:
				if int(n) > int(version[index]):
					update = True
					break
				elif int(n) < int(version[index]):
					break
				index += 1
			
			updateMessageDialog = QtGui.QDialog(self)
			vBoxLayout = QtGui.QVBoxLayout(updateMessageDialog)

			textLabel = QtGui.QLabel(updateMessageDialog)
			textLabel.setTextFormat(QtCore.Qt.RichText)
			textLabel.setOpenExternalLinks(True)
			textLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
			vBoxLayout.addWidget(textLabel)
				
			buttonBox = QtGui.QDialogButtonBox(updateMessageDialog)
			buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
			buttonBox.setCenterButtons(True)
			QtCore.QObject.connect(buttonBox, QtCore.SIGNAL('accepted()'), updateMessageDialog.accept)
			vBoxLayout.addWidget(buttonBox)

			if update:
				updateMessageDialog.setWindowTitle('New update')
				textLabel.setText("""<b>New update available!</b>
									 <br/><br/>Your version: <b>v%s</b>
									 <br/><br/>Current version: <b>v%s</b>
									 <br/><br/><a href="http://github.com/Moussekateer/TF2IdleGUI">Read the latest changes</a>.
									 <br/><br/><a href="http://github.com/Moussekateer/TF2IdleGUI/downloads">Download the newest version</a>.<br/><br/>"""
									 % (Version.version, currentversion))
			else:
				updateMessageDialog.setWindowTitle('No update')
				textLabel.setText("""You have the latest version.
									 <br/><br/>Your version: <b>v%s</b>
									 <br/><br/>Current version: <b>v%s</b><br/><br/>"""
									 % (Version.version, currentversion))

			updateMessageDialog.show()

	def showAbout(self):
		about = AboutDialog(self)
		about.exec_()

class AboutDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('About')
		self.gridLayout = QtGui.QGridLayout(self)

		self.imageLabel = ClickableLabel(self)
		self.imageLabel.setPixmap(QtGui.QPixmap(returnResourcePath('images/tf2idle.png')))
		self.gridLayout.addWidget(self.imageLabel, 0, 0, 1, 1)
		
		self.textLabel = QtGui.QLabel(self)
		self.textLabel.setTextFormat(QtCore.Qt.RichText)
		self.textLabel.setText("""<b>TF2Idle v%s</b><br/><br/>Developed by <a href="http://steamcommunity.com/id/Moussekateer">Moussekateer</a>.
								  <br/><br/>Thanks to <a href="http://steamcommunity.com/id/WindPower">WindPower</a> (aka the witch) for his limitless Python knowledge.
								  <br/><br/>Thanks to <a href="http://steamcommunity.com/id/rjackson">RJackson</a> for contributing code to TF2Idle.
								  <br/><br/>Some images used were extracted from TF2 and are the property of <a href="http://www.valvesoftware.com">Valve</a>.
								  <br/><br/>Some images used were created by <a href="http://fabrydesign.com">Wade 'Nineaxis' Fabry</a>.
								  <br/><br/>They are kredit to team.""" % Version.version)
		self.textLabel.setOpenExternalLinks(True)
		self.gridLayout.addWidget(self.textLabel, 0, 1, 1, 1)

		self.licenseImage = QtGui.QLabel()
		self.licenseImage.setPixmap(QtGui.QPixmap(returnResourcePath('images/creative_commons.png')))
		self.gridLayout.addWidget(self.licenseImage, 1, 0, 1, 1)

		self.licenseLabel = QtGui.QLabel(self)
		self.licenseLabel.setTextFormat(QtCore.Qt.RichText)
		self.licenseLabel.setText("""<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">TF2Idle</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://steamcommunity.com/id/moussekateer" property="cc:attributionName" rel="cc:attributionURL">Moussekateer</a> is licensed under a<br/><a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>.""")
		self.licenseLabel.setOpenExternalLinks(True)
		self.gridLayout.addWidget(self.licenseLabel, 1, 1, 1, 1)

		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)

class UpdateCheckThread(QtCore.QThread):
	def __init__(self, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.URL = r'http://tf2notifications.appspot.com/TF2Idleversion'

	def run(self):
		try:
			current_version = urllib2.urlopen(self.URL, timeout=5).read()
			self.emit(QtCore.SIGNAL('recievedVersion'), current_version)
		except:
			self.emit(QtCore.SIGNAL('recievedVersion'), None)

class ClickableLabel(QtGui.QLabel):
	def __init__(self, parent=None):
		QtGui.QLabel.__init__(self, parent)
	
	def mouseDoubleClickEvent(self, event):
		stoat = Stoat(self)
		stoat.exec_()

class Stoat(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('Secret Stoat')
		self.vBoxLayout = QtGui.QVBoxLayout(self)
		
		self.imageLabel = QtGui.QLabel(self)
		self.imageLabel.setPixmap(QtGui.QPixmap(returnResourcePath('images/secret_stoat.png')))
		self.vBoxLayout.addWidget(self.imageLabel)
		
		self.textLabel = QtGui.QLabel(self)
		self.textLabel.setText("""Praise the <b>Secret Stoat</b> and all it stands for: <b>WIN</b>.<br/>
							      Definitions of <b>WIN</b> on the Web:<br/><br/>
								  - be the winner in a contest or competition; be victorious; "He won the Gold Medal in skating"; "Our home team won"; "Win the game"<br/>
								  - acquire: win something through one\'s efforts; "I acquired a passing knowledge of Chinese"; "Gain an understanding of international finance"<br/>
								  - gain: obtain advantages, such as points, etc.; "The home team was gaining ground"<br/>
								  - a victory (as in a race or other competition); "he was happy to get the win"<br/>
								  - winnings: something won (especially money)<br/>
								  - succeed: attain success or reach a desired goal; "The enterprise succeeded"; "We succeeded in getting tickets to the show"; "she struggled to overcome her handicap and won"
								  """)
		self.textLabel.setWordWrap(True)
		self.textLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		self.vBoxLayout.addWidget(self.textLabel)

class SettingsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_SettingsDialog(self)