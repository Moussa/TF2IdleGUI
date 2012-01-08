import Config
from PyQt4 import QtCore, QtGui
from AccountDialog import Ui_AccountDialog

optionsfile = 'tf2idle.ini'
settings = Config.settings(optionsfile)

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

class Ui_MainWindow(object):
	def __init__(self, MainWindow):
		# Create MainWindow
		self.MainWindow = MainWindow
		self.MainWindow.setObjectName('MainWindow')
		self.MainWindow.resize(700, 400)
		self.MainWindow.setWindowTitle('TF2Idle')
		
		# Add Tool bar
		self.toolBar = QtGui.QToolBar(self.MainWindow)
		self.toolBar.setObjectName('toolBar')
		self.toolBar.setIconSize(QtCore.QSize(40, 40))
		self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("tf2logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		
		self.addAccountAction = self.toolBar.addAction(icon, 'Add account')
		QtCore.QObject.connect(self.addAccountAction, QtCore.SIGNAL('triggered()'), self.openAccountDialog)
		
		self.editAccountAction = self.toolBar.addAction(icon, 'Edit account')
		QtCore.QObject.connect(self.editAccountAction, QtCore.SIGNAL('triggered()'), curry(self.openAccountDialog, editAccount=True))
		
		self.toolBar.addAction(icon, 'Start idling')
		self.toolBar.addAction(icon, 'Start log dropper')
		self.toolBar.addAction(icon, 'Delete accounts')
		self.MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)
		
		# Create layout widget and attach to MainWindow
		self.centralwidget = QtGui.QWidget(self.MainWindow)
		self.centralwidget.setObjectName('centralwidget')
		self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, self.MainWindow.width()-self.toolBar.width(), self.MainWindow.height()))
		self.verticalLayoutWidget.setObjectName('verticalLayoutWidget')
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setMargin(0)
		self.verticalLayout.setObjectName('verticalLayout')
		self.MainWindow.setCentralWidget(self.centralwidget)
		
		# Add menu bar
		self.menubar = QtGui.QMenuBar(self.MainWindow)
		self.menubar.setObjectName('menubar')
		self.MainWindow.setMenuBar(self.menubar)
		
		# Add status bar
		#self.statusbar = QtGui.QStatusBar(self.MainWindow)
		#self.statusbar.setObjectName('statusbar')
		#self.MainWindow.setStatusBar(self.statusbar)
		
		# Add File menu
		menu = self.addMenu('File')
		self.addSubMenu(menu, 'Exit', text='Exit', statustip='Exit TF2Idle', shortcut='Ctrl+Q', action={'trigger':'triggered()', 'action':MainWindow.close})
		
		# Add Accounts menu
		menu = self.addMenu('Accounts')
		self.addSubMenu(menu, 'Add account', text='Add account', statustip='Add a Steam account', shortcut='Ctrl+A', action={'trigger':'triggered()', 'action':self.openAccountDialog})
		menu.addSeparator()
		#result = self.menubar.findChild(QtGui.QMenuBar, QtCore.QString('Accounts'))
		
		# Add Backpack menu
		self.addMenu('Backpack')
		
		# Add About menu
		self.addMenu('About')
		
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
		
		self.updateAccountBoxes()

	def updateAccountBoxes(self):
		widgets = self.verticalLayoutWidget.findChildren(QtGui.QCommandLinkButton)
		checkedbuttons = []
		for widget in widgets:
			if widget.isChecked():
				checkedbuttons.append(str(widget.text()))
			widget.close()

		row = 0
		column = 0
		numperrow = 4
		buttonheight = self.verticalLayoutWidget.height()/6
		for account in settings.get_sections():
			settings.set_section(account)
			accountname = settings.get_option('steam_username')
			self.commandLinkButton = QtGui.QCommandLinkButton(self.verticalLayoutWidget)
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap('tf2logo.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.commandLinkButton.setIcon(icon)
			self.commandLinkButton.setGeometry(QtCore.QRect(column*self.verticalLayoutWidget.width()/numperrow, row*buttonheight, self.verticalLayoutWidget.width()/numperrow, buttonheight))
			self.commandLinkButton.setCheckable(True)
			font = QtGui.QFont()
			# See why this doesn't work
			font.setFamily('TF2 Build')
			self.commandLinkButton.setFont(font)
			if accountname in checkedbuttons:
				self.commandLinkButton.setChecked(True)
			self.commandLinkButton.setObjectName('commandLinkButton' + accountname)
			self.commandLinkButton.setText(accountname)
			self.commandLinkButton.show()
			column += 1
			if column == numperrow:
				row += 1
				column = 0
		

	def addMenu(self, menuname):
		self.menu = QtGui.QMenu(self.menubar)
		self.menu.setObjectName('menu' + menuname)
		self.menu.setTitle(menuname)
		self.menubar.addAction(self.menu.menuAction())
		return self.menu
	
	def addSubMenu(self, menu, menuname, shortcut=None, text=None, tooltip=None, statustip=None, action=None):
		self.action = QtGui.QAction(self.MainWindow)
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
	
	def openAccountDialog(self, editAccount=False):
		if editAccount:
			widgets = self.verticalLayoutWidget.findChildren(QtGui.QCommandLinkButton)
			checkedbuttons = []
			for widget in widgets:
				if widget.isChecked():
					checkedbuttons.append(str(widget.text()))
			if len(checkedbuttons) == 0:
				QtGui.QMessageBox.information(self.MainWindow, 'No accounts selected', 'Please select an account to edit')
			elif len(checkedbuttons) > 1:
				QtGui.QMessageBox.information(self.MainWindow, 'More than one account selected', 'Please select a single account to edit')
			else:
				dialogWindow = AccountDialogWindow(account='Account-'+checkedbuttons[0])
				dialogWindow.setModal(True)
				dialogWindow.exec_()
				self.updateAccountBoxes()
		else:
			dialogWindow = AccountDialogWindow()
			dialogWindow.setModal(True)
			dialogWindow.exec_()
			self.updateAccountBoxes()
	
class AccountDialogWindow(QtGui.QDialog):
	def __init__(self, account=None, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AccountDialog(self, settings, account)