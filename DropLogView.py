import Config, tf2, time, os, webbrowser
from PyQt4 import QtCore, QtGui

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

class DropLogView(QtGui.QWidget):
	def __init__(self, mainwindow):
		QtGui.QWidget.__init__(self)
		self.mainwindow = mainwindow
		self.settings = Config.settings
		self.logWindow = QtGui.QTextBrowser()
		self.logWindow.setOpenLinks(False)
		self.accountThreads = {}
		self.eventsList = []
		self.selectedAccounts = []
		
		#greyoutfont = QtGui.QFont()
		#greyoutfont.setItalic(True)
		logWindowStyle = 'background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);'
		self.logWindow.setStyleSheet(logWindowStyle)
		self.logWindow.setReadOnly(True)
		
		self.updateWindow(construct = True)

	def updateWindow(self, construct=False, disableUpdateGCFs=False):

		# Add horizontal toolbar actions
		switchToAccountsViewIcon = QtGui.QIcon()
		switchToAccountsViewIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.switchToAccountsViewAction = self.mainwindow.htoolBar.addAction(switchToAccountsViewIcon, 'Accounts view')
		QtCore.QObject.connect(self.switchToAccountsViewAction, QtCore.SIGNAL('triggered()'), self.changeMainWindowView)
		
		self.mainwindow.htoolBar.addSeparator()
		
		addAccountsIcon = QtGui.QIcon()
		addAccountsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.addAccountsAction = self.mainwindow.htoolBar.addAction(addAccountsIcon, 'Add accounts')
		QtCore.QObject.connect(self.addAccountsAction, QtCore.SIGNAL('triggered()'), self.addAccounts)
		
		removeAccountsIcon = QtGui.QIcon()
		removeAccountsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.removeAccountsAction = self.mainwindow.htoolBar.addAction(removeAccountsIcon, 'Remove accounts')
		QtCore.QObject.connect(self.removeAccountsAction, QtCore.SIGNAL('triggered()'), self.removeAccounts)
		
		self.mainwindow.htoolBar.addSeparator()

		RemoveAllAccountsIcon = QtGui.QIcon()
		RemoveAllAccountsIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.RemoveAllAccountsAction = self.mainwindow.htoolBar.addAction(RemoveAllAccountsIcon, 'Remove all accounts')
		QtCore.QObject.connect(self.RemoveAllAccountsAction, QtCore.SIGNAL('triggered()'), self.stopLogging)

		if construct:
			self.gridLayout = QtGui.QGridLayout(self)
			self.gridLayout.setMargin(0)
			
			self.verticalLayout = QtGui.QVBoxLayout()
			self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
			self.gridLayout.addWidget(self.logWindow)
			
			QtCore.QObject.connect(self.logWindow, QtCore.SIGNAL('anchorClicked(QUrl)'), self.openLink)
			
			QtCore.QMetaObject.connectSlotsByName(self)
	
	def getSelectedAccounts(self):
		self.emit(QtCore.SIGNAL('retrieveSelectedAccounts'))
		
	def setSelectedAccounts(self, selectedAccounts):
		self.selectedAccounts = selectedAccounts
	
	def changeMainWindowView(self):
		self.mainwindow.changeView('accounts')

	def addAccounts(self):
		self.getSelectedAccounts()
		for account in self.selectedAccounts:
			if account not in self.accountThreads:
				self.thread = DropMonitorThread(account)
				QtCore.QObject.connect(self.thread, QtCore.SIGNAL('logEvent(PyQt_PyObject)'), self.addEvent)
				QtCore.QObject.connect(self.thread, QtCore.SIGNAL('threadDeath'), self.removeThread)
				self.accountThreads[account] = self.thread
				self.thread.start()

	def removeAccounts(self):
		self.getSelectedAccounts()
		for account in self.selectedAccounts:
			if account in self.accountThreads:
				self.accountThreads[account].kill()

	def stopLogging(self):
		for account in self.accountThreads:
			self.accountThreads[account].kill()

	def addEvent(self, event):
		self.eventsList.append(event)
		self.updateLogDisplay()

	def removeThread(self, account):
		del self.accountThreads[account]

	def addText(self, text):
		self.eventsList.append(text)
		self.logWindow.setText(self.dropsString)
	
	def openLink(self, url):
		webbrowser.open(url.toString())
	
	def returnItemLink(self, steam_id, item_id, colour):
		self.settings.set_section('Settings')
		backpack_viewer = self.settings.get_option('backpack_viewer')
		
		if backpack_viewer == 'OPTF2':
			return '<a style="color: #%s" href="http://optf2.com/tf2/item/%s/%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'Steam':
			return '<a style="color: #%s" href="http://steamcommunity.com/profiles/%s/inventory/#440_2_%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'TF2B':
			return '<a style="color: #%s" href="http://tf2b.com/item/%s/%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'TF2Items':
			return '<a style="color: #%s" href="http://www.tf2items.com/item/%s">Link</a>' % (colour, item_id)
			
	def addTableRow(self, event):
		if event['event_type'] != 'system_message':
			self.settings.set_section('Account-' + event['account'])
			colour = self.settings.get_option('ui_log_colour')
		tableRow = '<tr>'

		if event['event_type'] == 'system_message':
			tableRow += '<td ALIGN="center" >' + event['message'] + '</td>'
			tableRow += '<td></td>'
			tableRow += '<td></td>'
			tableRow += '<td></td>'
			tableRow += '<td ALIGN="center" >' + event['time'] + '</td>'
		elif event['event_type'] == 'weapon_drop':
			tableRow += '<td ALIGN="center" ><font color=#%s>Weapon</font></td>' % colour
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['item'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + self.returnItemLink(event['steam_id'], event['item_id'], colour) + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['display_name'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['time'] + '</font></td>'

		tableRow += '</tr>'
		return tableRow

	def updateLogDisplay(self):
		display_string = """<table width=100%>
							<tr>
							<th>Type</th>
							<th>Item</th>
							<th>Item Link</th>
							<th>Account</th>
							<th>Time</th>
							</tr>"""
		for event in reversed(self.eventsList):
			display_string += self.addTableRow(event)
		display_string += """</table>"""

		self.logWindow.setHtml(display_string)

class DropMonitorThread(QtCore.QThread):
	def __init__(self, account, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.account = account
		self.settings.set_section('Settings')
		self.APIKey = self.settings.get_option('API_key')
		self.settings.set_section('Account-' + self.account)
		self.id = tf2._getSteamID64(self.settings.get_option('steam_vanityid'))
		if self.settings.get_option('account_nickname') != '':
			self.displayname = self.settings.get_option('account_nickname')
		else:
			self.displayname = self.account
		self.itemCount = 0
		self.crateCount = 0
		self.keepThreadAlive = True
		self.API = tf2.API(key=self.APIKey)
		self.lastID = None

	def returnNewestItem(self):
		self.API.getProfile(self.id)
		self.API.getBackpack(self.id)
		backpack = self.API.users[self.id]['backpack']
		allbackpack = backpack.placed + backpack.unplaced
		templist = []
		for z in allbackpack:
			templist.append(z['id'])
		newestitem = allbackpack[templist.index(max(templist))]
		return newestitem

	def kill(self):
		self.keepThreadAlive = False

	def run(self):
		self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'system_message', 'message': 'Logging on ' + self.displayname, 'time': time.strftime('%H:%M', time.localtime(time.time()))})
		while self.keepThreadAlive:
			if self.lastID is None:
				self.lastID = self.returnNewestItem()['id']
			else:
				try:
					newestitem = self.returnNewestItem()
					# Check to see if item with highest ID has changed
					if newestitem['id'] != self.lastID:
						self.lastID = newestitem['id']
						self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'weapon_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})
						if newestitem['item_class'] != 'supply_crate' and newestitem['item_name'] != 'Salvaged Mann Co. Supply Crate':
							self.emit(QtCore.SIGNAL('FoundItem'), output)
							self.itemCount += 1
						else:
							self.emit(QtCore.SIGNAL('FoundCrate'), output)
							self.crateCount += 1
				except:
					pass
			time.sleep(10)
		self.emit(QtCore.SIGNAL('threadDeath'), self.account)