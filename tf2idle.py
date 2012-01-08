import sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow

optionsfile = 'tf2idle.ini'
settings = Config.settings(optionsfile)

class MainWindow(QtGui.QMainWindow):
	def __init__(self, settings, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.window = Ui_MainWindow(self, settings)
		
if __name__ == "__main__":
	try:
		open(optionsfile)
	except IOError:
		settings.set_section('Settings')
		settings.add_section()
		settings.set_option('launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow(settings)
	myapp.show()
	
	sys.exit(app.exec_())