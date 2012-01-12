import os, sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import MainWindow

optionsfile = 'tf2idle.ini'

def setDefaultSettings():
	Config.settings.set_section('Settings')
	if not Config.settings.has_section('Settings'):
		Config.settings.add_section()
	if not Config.settings.has_option('steam_location'):
		Config.settings.set_option('steam_location', 'C:/Program Files (x86)/Steam')
	if not Config.settings.has_option('secondary_steamapps_location'):
		Config.settings.set_option('secondary_steamapps_location', '')
	if not Config.settings.has_option('sandboxie_location'):
		Config.settings.set_option('sandboxie_location', 'C:/Program Files/Sandboxie')
	if not Config.settings.has_option('API_key'):
		Config.settings.set_option('API_key', '')
	if not Config.settings.has_option('backpack_viewer') or Config.settings.get_option('backpack_viewer') == '':
		Config.settings.set_option('backpack_viewer', 'OPTF2')
	if not Config.settings.has_option('launch_options'):
		Config.settings.set_option('launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	if not Config.settings.has_option('ui_no_of_columns') or Config.settings.get_option('ui_no_of_columns') == '':
		Config.settings.set_option('ui_no_of_columns', '2')
	Config.settings.flush_configuration()
		
if __name__ == "__main__":
	Config.init(optionsfile)
	setDefaultSettings()
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	returnCode = app.exec_()
	Config.settings.flush_configuration()
	sys.exit(returnCode)