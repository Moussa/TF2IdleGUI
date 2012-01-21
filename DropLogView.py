import Config, tf2, time, os, webbrowser
from PyQt4 import QtCore, QtGui
from LogEntriesDialog import Ui_LogEntriesDialog

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
		self.hatCount = 0
		self.weaponCount = 0
		self.toolCount = 0
		self.crateCount = 0

		logWindowStyle = 'background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);'
		self.logWindow.setStyleSheet(logWindowStyle)
		self.logWindow.setReadOnly(True)

		self.updateWindow(construct = True)

	def updateWindow(self, construct=False):

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

		stopLoggingIcon = QtGui.QIcon()
		stopLoggingIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.stopLoggingAction = self.mainwindow.htoolBar.addAction(stopLoggingIcon, 'Stop logging')
		QtCore.QObject.connect(self.stopLoggingAction, QtCore.SIGNAL('triggered()'), self.stopLogging)

		self.mainwindow.htoolBar.addSeparator()

		toggleLogEntriesIcon = QtGui.QIcon()
		toggleLogEntriesIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.toggleLogEntriesAction = self.mainwindow.htoolBar.addAction(toggleLogEntriesIcon, 'Toggle log entries')
		QtCore.QObject.connect(self.toggleLogEntriesAction, QtCore.SIGNAL('triggered()'), self.toggleEntries)
		
		saveToFileIcon = QtGui.QIcon()
		saveToFileIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.saveToFileAction = self.mainwindow.htoolBar.addAction(saveToFileIcon, 'Save to file')
		#QtCore.QObject.connect(self.saveToFileAction, QtCore.SIGNAL('triggered()'), self.saveToFile)
		
		self.mainwindow.htoolBar.addSeparator()
		
		resetCountIcon = QtGui.QIcon()
		resetCountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.resetCountAction = self.mainwindow.htoolBar.addAction(resetCountIcon, 'Reset count')
		QtCore.QObject.connect(self.resetCountAction, QtCore.SIGNAL('triggered()'), self.resetCount)
		
		font = QtGui.QFont()
		font.setFamily('TF2 Build')
		font.setPointSize(18)
		
		self.hatCounterwidget = QtGui.QWidget()
		self.hatCounterLayout = QtGui.QVBoxLayout(self.hatCounterwidget)

		self.hatCounter = QtGui.QLabel()
		self.hatCounter.setFont(font)
		self.hatCounter.setText(str(self.hatCount))
		self.hatCounter.setAlignment(QtCore.Qt.AlignCenter)

		self.hatCounterLabel = QtGui.QLabel()
		self.hatCounterLabel.setText('Hats')
		self.hatCounterLabel.setAlignment(QtCore.Qt.AlignCenter)
		
		self.hatCounterLayout.addWidget(self.hatCounter)
		self.hatCounterLayout.addWidget(self.hatCounterLabel)
		self.mainwindow.htoolBar.addWidget(self.hatCounterwidget)

		self.weaponCounterwidget = QtGui.QWidget()
		self.weaponCounterLayout = QtGui.QVBoxLayout(self.weaponCounterwidget)

		self.weaponCounter = QtGui.QLabel()
		self.weaponCounter.setFont(font)
		self.weaponCounter.setText(str(self.weaponCount))
		self.weaponCounter.setAlignment(QtCore.Qt.AlignCenter)

		self.weaponCounterLabel = QtGui.QLabel()
		self.weaponCounterLabel.setText('Weapons')
		self.weaponCounterLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.weaponCounterLayout.addWidget(self.weaponCounter)
		self.weaponCounterLayout.addWidget(self.weaponCounterLabel)
		self.mainwindow.htoolBar.addWidget(self.weaponCounterwidget)
		
		self.toolCounterwidget = QtGui.QWidget()
		self.toolCounterLayout = QtGui.QVBoxLayout(self.toolCounterwidget)

		self.toolCounter = QtGui.QLabel()
		self.toolCounter.setFont(font)
		self.toolCounter.setText(str(self.toolCount))
		self.toolCounter.setAlignment(QtCore.Qt.AlignCenter)

		self.toolCounterLabel = QtGui.QLabel()
		self.toolCounterLabel.setText('Tools')
		self.toolCounterLabel.setAlignment(QtCore.Qt.AlignCenter)
		
		self.toolCounterLayout.addWidget(self.toolCounter)
		self.toolCounterLayout.addWidget(self.toolCounterLabel)
		self.mainwindow.htoolBar.addWidget(self.toolCounterwidget)
		
		self.crateCounterwidget = QtGui.QWidget()
		self.crateCounterLayout = QtGui.QVBoxLayout(self.crateCounterwidget)

		self.crateCounter = QtGui.QLabel()
		self.crateCounter.setFont(font)
		self.crateCounter.setText(str(self.crateCount))
		self.crateCounter.setAlignment(QtCore.Qt.AlignCenter)

		self.crateCounterLabel = QtGui.QLabel()
		self.crateCounterLabel.setText('Crates')
		self.crateCounterLabel.setAlignment(QtCore.Qt.AlignCenter)
		
		self.crateCounterLayout.addWidget(self.crateCounter)
		self.crateCounterLayout.addWidget(self.crateCounterLabel)
		self.mainwindow.htoolBar.addWidget(self.crateCounterwidget)

		if construct:
			self.gridLayout = QtGui.QGridLayout(self)
			self.gridLayout.setMargin(0)

			self.verticalLayout = QtGui.QVBoxLayout()
			self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
			self.gridLayout.addWidget(self.logWindow)

			QtCore.QObject.connect(self.logWindow, QtCore.SIGNAL('anchorClicked(QUrl)'), self.openLink)

			QtCore.QMetaObject.connectSlotsByName(self)

			self.updateLogDisplay()

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

	def toggleEntries(self):
		logEntriesWindow = LogEntriesWindow()
		logEntriesWindow.setModal(True)
		logEntriesWindow.exec_()
		self.updateLogDisplay()
	
	def resetCount(self):
		self.hatCount = 0
		self.weaponCount = 0
		self.toolCount = 0
		self.crateCount = 0

		self.hatCounter.setText(str(self.hatCount))
		self.weaponCounter.setText(str(self.weaponCount))
		self.toolCounter.setText(str(self.toolCount))
		self.crateCounter.setText(str(self.crateCount))

	def addEvent(self, event):
		if event['event_type'] == 'weapon_drop':
			self.weaponCount += 1
		elif event['event_type'] == 'crate_drop':
			self.crateCount += 1
		elif event['event_type'] == 'hat_drop':
			self.hatCount += 1
		elif event['event_type'] == 'tool_drop':
			self.toolCount += 1
		self.eventsList.append(event)
		self.updateLogDisplay()

	def removeThread(self, account):
		del self.accountThreads[account]

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
		self.settings.set_section('Settings')
		toggles = self.settings.get_option('ui_log_entry_toggles').split(',')

		if event['event_type'] != 'system_message':
			self.settings.set_section('Account-' + event['account'])
			colour = self.settings.get_option('ui_log_colour')

		tableRow = '<tr>'
		if event['event_type'] == 'system_message' and 'system' in toggles:
			tableRow += '<td ALIGN="center" >' + event['message'] + '</td>'
			tableRow += '<td></td>'
			tableRow += '<td></td>'
			tableRow += '<td></td>'
			tableRow += '<td ALIGN="center" >' + event['time'] + '</td>'
		elif event['event_type'] == 'weapon_drop' and 'weapons' in toggles:
			tableRow += '<td ALIGN="center" ><font color=#%s>Weapon</font></td>' % colour
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['item'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + self.returnItemLink(event['steam_id'], event['item_id'], colour) + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['display_name'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['time'] + '</font></td>'
		elif event['event_type'] == 'crate_drop' and 'crates' in toggles:
			tableRow += '<td ALIGN="center" ><font color=#%s>Crate</font></td>' % colour
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['item'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + self.returnItemLink(event['steam_id'], event['item_id'], colour) + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['display_name'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['time'] + '</font></td>'
		elif event['event_type'] == 'hat_drop' and 'hats' in toggles:
			tableRow += '<td ALIGN="center" ><font color=#%s>Hat</font></td>' % colour
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['item'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + self.returnItemLink(event['steam_id'], event['item_id'], colour) + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['display_name'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['time'] + '</font></td>'
		elif event['event_type'] == 'tool_drop' and 'tools' in toggles:
			tableRow += '<td ALIGN="center" ><font color=#%s>Tool</font></td>' % colour
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['item'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + self.returnItemLink(event['steam_id'], event['item_id'], colour) + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['display_name'] + '</font></td>'
			tableRow += '<td ALIGN="center" ><font color=#%s>' % colour + event['time'] + '</font></td>'
		tableRow += '</tr>'

		if tableRow == '<tr></tr>':
			return None
		else:
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
			tableRow = self.addTableRow(event)
			if tableRow is not None:
				display_string += tableRow
		display_string += """</table>"""

		self.logWindow.setHtml(display_string)

		self.hatCounter.setText(str(self.hatCount))
		self.weaponCounter.setText(str(self.weaponCount))
		self.toolCounter.setText(str(self.toolCount))
		self.crateCounter.setText(str(self.crateCount))

class DropMonitorThread(QtCore.QThread):
	def __init__(self, account, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.account = account
		self.settings.set_section('Settings')
		self.APIKey = self.settings.get_option('API_key')
		self.settings.set_section('Account-' + self.account)
		if self.settings.get_option('account_nickname') != '':
			self.displayname = self.settings.get_option('account_nickname')
		else:
			self.displayname = self.account
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
		self.settings.set_section('Account-' + self.account)
		self.id = tf2._getSteamID64(self.settings.get_option('steam_vanityid'))

		self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'system_message', 'message': 'Logging on ' + self.displayname, 'time': time.strftime('%H:%M', time.localtime(time.time()))})
		while self.keepThreadAlive:
			if self.lastID is None:
				self.lastID = self.returnNewestItem()['id']
			else:
				try:
					newestitem = self.returnNewestItem()
					#self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'weapon_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})

					if newestitem['id'] != self.lastID:
						self.lastID = newestitem['id']
						if newestitem['item_class'] == 'tf_wearable':
							self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'hat_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})
						elif newestitem['item_class'] == 'supply_crate':
							self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'crate_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})
						elif newestitem['item_class'] == 'tool':
							self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'tool_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})
						else:
							self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'weapon_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})
				except:
					pass
			time.sleep(5)
		self.emit(QtCore.SIGNAL('threadDeath'), self.account)
		self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'system_message', 'message': 'Stopped logging on ' + self.displayname, 'time': time.strftime('%H:%M', time.localtime(time.time()))})

class LogEntriesWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_LogEntriesDialog(self)