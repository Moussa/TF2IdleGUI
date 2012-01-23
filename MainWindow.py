import Config, os
import Sandboxie
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
		self.menubar = QtGui.QMenuBar(self)
		self.menubar.setObjectName('menubar')
		self.setMenuBar(self.menubar)
		
		# Add File menu
		filemenu = self.addMenu('File')
		self.addSubMenu(filemenu, 'Settings', text='Settings', statustip='Open settings', shortcut='Ctrl+S', action={'trigger':'triggered()', 'action':self.openSettings})
		filemenu.addSeparator()
		self.addSubMenu(filemenu, 'Exit', text='Exit', statustip='Exit TF2Idle', shortcut='Ctrl+Q', action={'trigger':'triggered()', 'action':self.close})
		
		# Add About menu
		aboutmenu = self.addMenu('About')
		self.addSubMenu(aboutmenu, 'Credits', text='Credits', statustip='See credits', action={'trigger':'triggered()', 'action':self.showCredits})
		
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
		self.settings.set_option('Settings', 'ui_window_size', '(%s, %s)' % (self.width(), self.height()))
		if self.sandboxieINIIsModified:
			Sandboxie.restoreSandboxieINI()

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
		self.menu = QtGui.QMenu(self.menubar)
		self.menu.setObjectName('menu' + menuname)
		self.menu.setTitle(menuname)
		self.menubar.addAction(self.menu.menuAction())
		return self.menu
	
	def addSubMenu(self, menu, menuname, shortcut=None, text=None, tooltip=None, statustip=None, action=None):
		self.action = QtGui.QAction(self)
		if shortcut:
			self.action.setShortcut(shortcut)
		self.action.setObjectName('action' + menuname)
		menu.addAction(self.action)
		if action:
			QtCore.QObject.connect(self.action, QtCore.SIGNAL(action['trigger']), action['action'])
		if text:
			self.action.setText(text)
		if tooltip:
			self.action.setToolTip(tooltip)
		if statustip:
			self.action.setStatusTip(statustip)
	
	def openSettings(self):
		dialogWindow = SettingsDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.accountsView.updateAccountBoxes()
		self.dropLogView.updateLogDisplay()

	def showCredits(self):
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
		self.textLabel.setText("""<b>TF2Idle 1.0</b><br/><br/>Developed by <a href="http://steamcommunity.com/id/Moussekateer">Moussekateer</a>
								  <br/><br/>Thanks to <a href="http://steamcommunity.com/id/WindPower">WindPower</a> (aka the witch) for his limitless Python knowledge.
								  <br/><br/>Thanks to <a href="http://steamcommunity.com/id/rjackson">RJackson</a> for contributing code to TF2Idle.
								  <br/><br/>Thanks to <a href="http://wiki.teamfortress.com">official TF2 wiki</a> for the \'borrowed\' icons.
								  <br/><br/>They are kredit to team.""")
		self.textLabel.setOpenExternalLinks(True)
		self.gridLayout.addWidget(self.textLabel, 0, 1, 1, 1)
		
		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setCenterButtons(False)
		self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)

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
		self.imageLabel.setPixmap(QtGui.QPixmap(returnResourcePath('images/secret_stoat.jpg')))
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