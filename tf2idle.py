import os, sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow

optionsfile = 'tf2idle.ini'

def setDefaultSettings():
	Config.settings.set_section('Settings')
	Config.settings.add_section()
	Config.settings.set_option('steam_location', 'C:/Program Files (x86)/Steam')
	Config.settings.set_option('secondary_steam_location', '')
	Config.settings.set_option('sandboxie_location', 'C:/Program Files/Sandboxie')
	Config.settings.set_option('API_key', '')
	Config.settings.set_option('backpack_viewer', 'OPTF2')
	Config.settings.set_option('launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	Config.settings.set_option('ui_no_of_columns', '4')

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.window = Ui_MainWindow(self)
		
if __name__ == "__main__":
	Config.init(optionsfile)
	if not os.path.exists(optionsfile):
<<<<<<< HEAD
		setDefaultSettings()
=======
		Config.settings.set_section('Settings')
		Config.settings.add_section()
		Config.settings.set_option('launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
>>>>>>> 81ea82b1e03e204c1dcb3cfbd93852674030b0c5
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	returnCode = app.exec_()
	Config.settings.flush_configuration()
<<<<<<< HEAD
	sys.exit(returnCode)
=======
	sys.exit(returnCode)
>>>>>>> 81ea82b1e03e204c1dcb3cfbd93852674030b0c5
