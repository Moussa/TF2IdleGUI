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

	def showCredits(self):
		about = QtGui.QMessageBox(self)
		about.setWindowTitle('Credits')
		about.setIconPixmap(QtGui.QPixmap(returnResourcePath('images/tf2idle.png')))
		about.setTextFormat(QtCore.Qt.RichText)
		about.setText("""<b>TF2Idle 1.0</b><br/><br/>Developed by <a href="http://steamcommunity.com/id/Moussekateer">Moussekateer</a>
						 <br/><br/>Thanks to <a href="http://steamcommunity.com/id/WindPower">WindPower</a> (aka the witch) for his limitless Python knowledge.
						 <br/><br/>Thanks to <a href="http://steamcommunity.com/id/rjackson">RJackson</a> for contributing code to TF2Idle.
						 <br/><br/>Thanks to <a href="http://wiki.teamfortress.com">official TF2 wiki</a> for the \'borrowed\' icons.
						 <br/><br/>They are kredit to team.""")
		about.exec_()

class SettingsDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_SettingsDialog(self)