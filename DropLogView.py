import Config, tf2, time, os, webbrowser
from PyQt4 import QtCore, QtGui, QtWebKit
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
		QtCore.QObject.connect(self.saveToFileAction, QtCore.SIGNAL('triggered()'), self.saveToFile)
		
		self.mainwindow.htoolBar.addSeparator()
		
		resetCountIcon = QtGui.QIcon()
		resetCountIcon.addPixmap(QtGui.QPixmap(returnResourcePath('images/unselected_button.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.resetCountAction = self.mainwindow.htoolBar.addAction(resetCountIcon, 'Reset count')
		QtCore.QObject.connect(self.resetCountAction, QtCore.SIGNAL('triggered()'), self.resetCount)
		
		self.mainwindow.htoolBar.addSeparator()
		
		font = QtGui.QFont()
		font.setFamily('TF2 Build')
		font.setPointSize(25)
		
		self.hatCounterwidget = QtGui.QWidget()
		self.hatCounterLayout = QtGui.QVBoxLayout(self.hatCounterwidget)
		self.hatCounterLayout.setSpacing(0)
		self.hatCounterLayout.setContentsMargins(10, -1, 10, -1)

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
		self.weaponCounterLayout.setSpacing(0)
		self.weaponCounterLayout.setContentsMargins(10, -1, 10, -1)

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
		self.toolCounterLayout.setSpacing(0)
		self.toolCounterLayout.setContentsMargins(10, -1, 10, -1)

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
		self.crateCounterLayout.setSpacing(0)
		self.crateCounterLayout.setContentsMargins(10, -1, 10, -1)

		self.crateCounter = ClickableLabel()
		self.crateCounter.setFont(font)
		self.crateCounter.setText(str(self.crateCount))
		self.crateCounter.setAlignment(QtCore.Qt.AlignCenter)
		QtCore.QObject.connect(self.crateCounter, QtCore.SIGNAL('WhatsThatSound'), self.nomNomCat)

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
		APIKey = self.settings.get_option('Settings', 'API_key')
		if len(APIKey) != 32:
			QtGui.QMessageBox.warning(self.mainwindow, 'API key not valid', 'Your API key is not valid, please check you have entered it correctly')
			return None
		try:
			API = tf2.API(key=APIKey)
			API.getProfile(76561197960435530)
		except:
			QtGui.QMessageBox.warning(self.mainwindow, 'API key not valid', 'Your API key is not valid, please check you have entered it correctly')
			return None
		self.getSelectedAccounts()
		if len(self.selectedAccounts) == 0:
			QtGui.QMessageBox.information(self.mainwindow, 'No accounts selected', 'Please select at least one account from the accounts page to add')
			return None
		for account in self.selectedAccounts:
			if account not in self.accountThreads:
				self.thread = DropMonitorThread(account)
				QtCore.QObject.connect(self.thread, QtCore.SIGNAL('logEvent(PyQt_PyObject)'), self.addEvent)
				QtCore.QObject.connect(self.thread, QtCore.SIGNAL('threadDeath'), self.removeThread)
				self.accountThreads[account] = self.thread
				self.thread.start()

	def removeAccounts(self):
		self.getSelectedAccounts()
		if len(self.selectedAccounts) == 0:
			QtGui.QMessageBox.information(self.mainwindow, 'No accounts selected', 'Please select at least one account from the accounts page to remove')
			return None
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
	
	def saveToFile(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save log to file', '', '.txt')
		if filename:
			toggles = self.settings.get_option('Settings', 'ui_log_entry_toggles').split(',')
			string = ''
			for event in self.eventsList:
				if event['event_type'] == 'system_message' and 'system' in toggles:
					string += '%s, %s\r\n' % (event['time'], event['message'])
				else:
					print_string = event['event_type'] == 'weapon_drop' and 'weapons' in toggles
					print_string = print_string or event['event_type'] == 'crate_drop' and 'crates' in toggles
					print_string = print_string or event['event_type'] == 'hat_drop' and 'hats' in toggles
					print_string = print_string or event['event_type'] == 'tool_drop' and 'tools' in toggles
					if print_string:
						string += '%s, %s, %s, %s, %s\r\n' % (event['time'], event['event_type'], event['item'], event['item_id'], event['display_name'])
			f = open(filename, 'wb')
			f.write(string.encode('utf8'))
			f.close()

	def openLink(self, url):
		webbrowser.open(url.toString())

	def returnItemLink(self, steam_id, item_id, colour):
		backpack_viewer = self.settings.get_option('Settings', 'backpack_viewer')

		if backpack_viewer == 'OPTF2':
			return '<a style="color: #%s" href="http://optf2.com/tf2/item/%s/%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'Steam':
			return '<a style="color: #%s" href="http://steamcommunity.com/profiles/%s/inventory/#440_2_%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'TF2B':
			return '<a style="color: #%s" href="http://tf2b.com/item/%s/%s">Link</a>' % (colour, steam_id, item_id)
		elif backpack_viewer == 'TF2Items':
			return '<a style="color: #%s" href="http://www.tf2items.com/item/%s">Link</a>' % (colour, item_id)

	def addTableRow(self, event):
		toggles = self.settings.get_option('Settings', 'ui_log_entry_toggles').split(',')

		self.size = self.settings.get_option('Settings', 'ui_log_font_size')
		self.family = self.settings.get_option('Settings', 'ui_log_font_family')
		self.style = self.settings.get_option('Settings', 'ui_log_font_style')
		self.weight = self.settings.get_option('Settings', 'ui_log_font_weight')
		self.colour = self.settings.get_option('Settings', 'ui_log_font_colour')
		if event['event_type'] != 'system_message':
			self.accountcolour = self.settings.get_option('Account-' + event['account'], 'ui_log_colour')

		if event['event_type'] == 'system_message' and 'system' in toggles:
			tableRow = """<tr style="color:#%s; font-family:'%s'; font-size:%spt;""" % (self.colour, self.family, self.size)
			if self.weight == '75':
				tableRow += 'font-weight:bold;'
			if self.style == '1':
				tableRow += 'font-style:italic;'
			tableRow += """">"""
			tableRow += """<td align='center' >""" + event['message'] + """</td>"""
			tableRow += """<td></td>"""
			tableRow += """<td></td>"""
			tableRow += """<td></td>"""
			tableRow +="""<td align='center' >""" + event['time'] + """</td>"""
		else:
			tableRow = """<tr style="color:#%s; font-family:'%s'; font-size:%spt;""" % (self.accountcolour, self.family, self.size)
			if self.weight == '75':
				tableRow += 'font-weight:bold;'
			if self.style == '1':
				tableRow += 'font-style:italic;'
			tableRow += """">"""
			if event['event_type'] == 'weapon_drop' and 'weapons' in toggles:
				tableRow += """<td align='center' >""" + 'Weapon' + """</td>"""
			elif event['event_type'] == 'crate_drop' and 'crates' in toggles:
				tableRow += """<td align='center' >""" + 'Crate' + """</td>"""
			elif event['event_type'] == 'hat_drop' and 'hats' in toggles:
				tableRow += """<td align='center' >""" + 'Hat' + """</td>"""
			elif event['event_type'] == 'tool_drop' and 'tools' in toggles:
				tableRow += """<td align='center' >""" + 'Tool' + """</td>"""
			else:
				# Nothing to display then
				return None
			tableRow += """<td align='center' >""" + event['item'] + """</td>"""
			tableRow += """<td align='center' >""" + self.returnItemLink(event['steam_id'], event['item_id'], self.accountcolour) + """</td>"""
			tableRow += """<td align='center' >""" + event['display_name'] + """</td>"""
			tableRow += """<td align='center' >""" + event['time'] + """</td>"""
			tableRow += """</tr>"""

		return tableRow

	def updateLogDisplay(self):
		logWindowStyle = 'background-color: #%s;color: #%s;' % (self.settings.get_option('Settings', 'ui_log_background_colour'), self.settings.get_option('Settings', 'ui_log_font_colour'))
		self.logWindow.setStyleSheet(logWindowStyle)

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

	def nomNomCat(self):
		videoPlayer = VideoDialog(self)
		videoPlayer.exec_()

class VideoDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom nom')
		self.resize(870, 496)
		self.vBoxLayout = QtGui.QVBoxLayout(self)
		self.vBoxLayout.setSpacing(0)
		self.vBoxLayout.setMargin(0)
		
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
		QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
		video = QtWebKit.QWebView()
		video.setHtml("""<iframe width="853" height="480" src="http://www.youtube.com/embed/OLsdhC9GdXQ?rel=0&autoplay=1&loop=1" frameborder="0" allowfullscreen></iframe>""")
		self.vBoxLayout.addWidget(video)

class DropMonitorThread(QtCore.QThread):
	def __init__(self, account, parent = None):
		QtCore.QThread.__init__(self, parent)
		self.settings = Config.settings
		self.account = account
		self.APIKey = self.settings.get_option('Settings', 'API_key')
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
		self.id = tf2._getSteamID64(self.settings.get_option('Account-' + self.account, 'steam_vanityid'))
		if self.settings.get_option('Account-' + self.account, 'account_nickname') != '':
			self.displayname = self.settings.get_option('Account-' + self.account, 'account_nickname')
		else:
			self.displayname = self.account

		self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'system_message', 'message': 'Logging on ' + self.displayname, 'time': time.strftime('%H:%M', time.localtime(time.time()))})
		while self.keepThreadAlive:
			try:
				if self.lastID is None:
					self.lastID = self.returnNewestItem()['id']
				newestitem = self.returnNewestItem()
				self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'weapon_drop', 'item': newestitem['item_name'].encode('utf8'), 'account': self.account, 'display_name': self.displayname, 'steam_id': self.id, 'item_id': newestitem['id'], 'time': time.strftime('%H:%M', time.localtime(time.time()))})

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
			# Allow thread death while sleeping
			timer = 0
			pollTime = int(self.settings.get_option('Settings', 'log_poll_time'))
			while self.keepThreadAlive and timer < 60 * pollTime: 
				time.sleep(1)
				timer += 1
		self.emit(QtCore.SIGNAL('threadDeath'), self.account)
		self.emit(QtCore.SIGNAL('logEvent(PyQt_PyObject)'), {'event_type': 'system_message', 'message': 'Stopped logging on ' + self.displayname, 'time': time.strftime('%H:%M', time.localtime(time.time()))})

class ClickableLabel(QtGui.QLabel):
	def __init__(self, parent=None):
		QtGui.QLabel.__init__(self, parent)
	
	def mouseDoubleClickEvent(self, event):
		self.emit(QtCore.SIGNAL('WhatsThatSound'))

class LogEntriesWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_LogEntriesDialog(self)