import sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.window = Ui_MainWindow(self)

class AccountDialogWindow(QtGui.QDialog):
	def __init__(self, parent=None, account=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_AccountDialog(self)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	
	#try:
	#	open(optionsfile)
	#except IOError as e:
	#	pass
		#Add wizard to force user to add settings
		#QtGui.QMessageBox.warning(self, 'Error', 'Settings file hasn\'t been created yet')
	
	sys.exit(app.exec_())