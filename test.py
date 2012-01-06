import sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow_ui import Ui_MainWindow
from AddAccountDialog_ui import Ui_AddAccountDialog

optionsfile = 'tf2idle.ini'
settings = Config.settings(optionsfile)

"""def errorDialog(title, message):
	message_box = QtGui.QMessageBox()
	message_box.setWindowTitle(title)
	message_box.setIcon(QtGui.QMessageBox.Warning)
	message_box.setText(message)
	message_box.setStandardButtons(QtGui.QMessageBox.Ok);
	message_box.exec_()"""

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
	
class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.updatemenus()
		self.updateaccountboxes()

	def updatemenus(self):
		self.ui.menuAccounts.clear()
		self.ui.setupUi(self)
		for account in settings.get_sections():
			settings.set_section(account)
			accountname = settings.get_option('steam_username')
			self.accountsubmenu = QtGui.QAction(self)
			self.accountsubmenu.setObjectName(accountname)
			self.accountsubmenu.setText(QtGui.QApplication.translate("MainWindow", accountname, None, QtGui.QApplication.UnicodeUTF8))
			self.ui.menuAccounts.addAction(self.accountsubmenu)
			QtCore.QObject.connect(self.accountsubmenu, QtCore.SIGNAL("triggered()"), curry(self.showAddAccountDialog, account='Account-' + accountname))
		QtCore.QObject.connect(self.ui.actionAdd_account, QtCore.SIGNAL("triggered()"), self.showAddAccountDialog)
		
	def updateaccountboxes(self):
		widgets = self.findChildren(QtGui.QCommandLinkButton)
		for widget in widgets:
			widget.close()

		row = 0
		column = 0
		numperrow = 3
		buttonheight = (self.height() - self.ui.menubar.height())/5
		for account in settings.get_sections():
			settings.set_section(account)
			accountname = settings.get_option('steam_username')
			self.commandLinkButton = QtGui.QCommandLinkButton(self)
			self.commandLinkButton.setGeometry(QtCore.QRect(column*self.width()/numperrow, (row*buttonheight) + self.ui.menubar.height(), self.width()/numperrow, buttonheight))
			self.commandLinkButton.setCheckable(True)
			self.commandLinkButton.setObjectName("commandLinkButton" + accountname)
			self.commandLinkButton.setText(QtGui.QApplication.translate("MainWindow", accountname, None, QtGui.QApplication.UnicodeUTF8))
			self.commandLinkButton.show()
			column += 1
			if column == numperrow:
				row += 1
				column = 0

	def showAddAccountDialog(self, account=None):
		dialogWindow = AddAccountDialogWindow(account=account)
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.updateaccountboxes()
		self.updatemenus()

class AddAccountDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None, account=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AddAccountDialog()
		self.ui.setupUi(self)
		
		if account:
			settings.set_section(account)
			self.ui.lineEdit.setText(settings.get_option('steam_username'))
			self.ui.lineEdit_2.setText(settings.get_option('steam_password'))
			self.ui.lineEdit_3.setText(settings.get_option('steam_vanityid'))
			self.ui.lineEdit_4.setText(settings.get_option('account_nickname'))
			self.ui.lineEdit_5.setText(settings.get_option('sandbox_name'))
			self.ui.lineEdit_6.setText(settings.get_option('sandbox_install'))
			self.ui.lineEdit_7.setText(settings.get_option('groups'))
			#change add button to ok
	
	def accept(self):
		steam_username = str(self.ui.lineEdit.text())
		steam_password = str(self.ui.lineEdit_2.text())
		steam_vanityid = str(self.ui.lineEdit_3.text())
		account_nickname = str(self.ui.lineEdit_4.text())
		sandbox_name = str(self.ui.lineEdit_5.text())
		sandbox_install = str(self.ui.lineEdit_6.text())
		groups = str(self.ui.lineEdit_7.text())
		
		if steam_username == '':
			QtGui.QMessageBox.warning(self, 'Error', 'Please enter a Steam username')
		elif steam_password == '':
			QtGui.QMessageBox.warning(self, 'Error', 'Please enter a Steam password')
		else:
			if steam_vanityid == '': # Try steam username as vanity ID
				steam_vanityid = steam_username
			if groups != '':
				groups_list = groups.replace(' ','').replace('.',',').split(',')
		
			if settings.has_section('Account-' + steam_username):
				QtGui.QMessageBox.warning(self, 'Error', 'Account already exists')
			else:
				settings.set_section('Account-' + steam_username)
				settings.add_section()
				settings.set_option('steam_username', steam_username)
				settings.set_option('steam_password', steam_password)
				settings.set_option('steam_vanityid', steam_vanityid)
				settings.set_option('account_nickname', account_nickname)
				settings.set_option('sandbox_name', sandbox_name)
				settings.set_option('sandbox_install', sandbox_install)
				settings.set_option('groups', groups)
				self.close()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	
	try:
		open(optionsfile)
	except IOError as e:
		pass
		#Add wizard to force user to add settings
		#QtGui.QMessageBox.warning(self, 'Error', 'Settings file hasn\'t been created yet')
	
	sys.exit(app.exec_())