import sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow_ui import Ui_MainWindow
from AddAccountDialog_ui import Ui_AddAccountDialog

optionsfile = 'tf2idle.ini'

def errorDialog(title, message):
	message_box = QtGui.QMessageBox()
	message_box.setWindowTitle(title)
	message_box.setIcon(QtGui.QMessageBox.Warning)
	message_box.setText(message)
	message_box.setStandardButtons(QtGui.QMessageBox.Ok);
	message_box.exec_()
	
class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.updatemenus()
			
	def updatemenus(self):
		self.ui.menuAccounts.clear()
		self.ui.setupUi(self)
		settings = Config.settings(optionsfile)
		for account in settings.get_sections():
			settings.set_section(account)
			self.accountsubmenu = QtGui.QAction(self)
			self.accountsubmenu.setObjectName(settings.get_option('steam_username'))
			self.accountsubmenu.setText(QtGui.QApplication.translate("MainWindow", settings.get_option('steam_username'), None, QtGui.QApplication.UnicodeUTF8))
			self.ui.menuAccounts.addAction(self.accountsubmenu)
			QtCore.QObject.connect(self.accountsubmenu, QtCore.SIGNAL("triggered()"), self.showAddAccountDialog)
		QtCore.QObject.connect(self.ui.actionAdd_account, QtCore.SIGNAL("triggered()"), self.showAddAccountDialog)
		
	def showAddAccountDialog(self, accountname=None):
		dialogWindow = AddAccountDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()
		self.updatemenus()

class AddAccountDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AddAccountDialog()
		self.ui.setupUi(self)
		self.settings = Config.settings(optionsfile)
		
		sender = str(self.sender().text())
		if self.settings.has_section('Account-' + sender):
			self.settings.set_section('Account-' + sender)
			self.ui.lineEdit.setText(self.settings.get_option('steam_username'))
			self.ui.lineEdit_2.setText(self.settings.get_option('steam_password'))
			self.ui.lineEdit_3.setText(self.settings.get_option('steam_vanityid'))
			self.ui.lineEdit_4.setText(self.settings.get_option('account_nickname'))
			self.ui.lineEdit_5.setText(self.settings.get_option('sandbox_name'))
			self.ui.lineEdit_6.setText(self.settings.get_option('sandbox_install'))
			self.ui.lineEdit_7.setText(self.settings.get_option('groups'))
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
		
			if self.settings.has_section('Account-' + steam_username):
				QtGui.QMessageBox.warning(self, 'Error', 'Account already exists')
			else:
				self.settings.set_section('Account-' + steam_username)
				self.settings.add_section()
				self.settings.set_option('steam_username', steam_username)
				self.settings.set_option('steam_password', steam_password)
				self.settings.set_option('steam_vanityid', steam_vanityid)
				self.settings.set_option('account_nickname', account_nickname)
				self.settings.set_option('sandbox_name', sandbox_name)
				self.settings.set_option('sandbox_install', sandbox_install)
				self.settings.set_option('groups', groups)
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