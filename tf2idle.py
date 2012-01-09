import os, sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow

optionsfile = 'tf2idle.ini'

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.window = Ui_MainWindow(self)
		
if __name__ == "__main__":
	Config.init(optionsfile)
	if not os.path.exists(optionsfile):
		Config.settings.set_section('Settings')
		Config.settings.add_section()
		Config.settings.set_option('launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	returnCode = app.exec_()
	Config.settings.flush_configuration()
	sys.exit(returnCode)
