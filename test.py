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
		QtCore.QObject.connect(self.ui.actionAdd_account, QtCore.SIGNAL("triggered()"), self.showAddAccountDialog)
		
		settings = Config.settings(optionsfile)
		for account in settings.get_sections():
			settings.set_section(account)
			self.account = QtGui.QAction(self)
			self.account.setObjectName(settings.get_option('steam_username'))
			self.account.setText(QtGui.QApplication.translate("MainWindow", settings.get_option('steam_username'), None, QtGui.QApplication.UnicodeUTF8))
			self.ui.menuAccounts.addAction(self.account)
		# Reupdate accounts menu here
		
	def showAddAccountDialog(self):
		dialogWindow = AddAccountDialogWindow()
		dialogWindow.setModal(True)
		dialogWindow.exec_()

class AddAccountDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AddAccountDialog()
		self.ui.setupUi(self)
	
	def accept(self):
		steam_username = str(self.ui.lineEdit.text())
		steam_password = str(self.ui.lineEdit_2.text())
		steam_vanityid = str(self.ui.lineEdit_4.text())
		account_nickname = str(self.ui.lineEdit_6.text())
		sandbox_name = str(self.ui.lineEdit_3.text())
		sandbox_install = str(self.ui.lineEdit_5.text())
		groups = str(self.ui.lineEdit_7.text())
		
		if steam_username == '':
			errorDialog('Error', 'Please enter a Steam username')
		elif steam_password == '':
			errorDialog('Error', 'Please enter a Steam password')
		else:
			if steam_vanityid == '': # Try steam username as vanity ID
				steam_vanityid = steam_username
			if groups != '':
				groups_list = groups.replace(' ','').replace('.',',').split(',')
		
			settings = Config.settings(optionsfile)
			if settings.has_section('Account-' + steam_username):
				errorDialog('Error', 'Account already exists')
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
		errorDialog('Error', 'Settings file hasn\'t been created yet')
	
	sys.exit(app.exec_())