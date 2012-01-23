import os, sys
import Config
from PyQt4 import QtCore, QtGui

from MainWindow import MainWindow

optionsfile = 'tf2idle.ini'

def setDefaultSettings():
	if not Config.settings.has_section('Settings'):
		Config.settings.add_section('Settings')
	if not Config.settings.has_option('Settings', 'steam_location'):
		Config.settings.set_option('Settings', 'steam_location', r'C:\Program Files (x86)\Steam')
	if not Config.settings.has_option('Settings', 'secondary_steamapps_location'):
		Config.settings.set_option('Settings', 'secondary_steamapps_location', '')
	if not Config.settings.has_option('Settings', 'sandboxie_location'):
		Config.settings.set_option('Settings', 'sandboxie_location', r'C:\Program Files\Sandboxie')
	if not Config.settings.has_option('Settings', 'API_key'):
		Config.settings.set_option('Settings', 'API_key', '')
	if not Config.settings.has_option('Settings', 'backpack_viewer') or Config.settings.get_option('Settings', 'backpack_viewer') == '':
		Config.settings.set_option('Settings', 'backpack_viewer', 'OPTF2')
	if not Config.settings.has_option('Settings', 'launch_options'):
		Config.settings.set_option('Settings', 'launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	if not Config.settings.has_option('Settings', 'easy_sandbox_mode') or Config.settings.get_option('Settings', 'easy_sandbox_mode') == '':
		Config.settings.set_option('Settings', 'easy_sandbox_mode', 'yes')
	if not Config.settings.has_option('Settings', 'ui_no_of_columns') or Config.settings.get_option('Settings', 'ui_no_of_columns') == '':
		Config.settings.set_option('Settings', 'ui_no_of_columns', '2')
	if not Config.settings.has_option('Settings', 'ui_window_size') or Config.settings.get_option('Settings', 'ui_window_size') == '':
		Config.settings.set_option('Settings', 'ui_window_size', '(694, 410)')
	if not Config.settings.has_option('Settings', 'ui_account_box_font_size') or Config.settings.get_option('Settings', 'ui_account_box_font_size') == '':
		Config.settings.set_option('Settings', 'ui_account_box_font_size', '12')
	if not Config.settings.has_option('Settings', 'ui_account_box_icon_size') or Config.settings.get_option('Settings', 'ui_account_box_icon_size') == '':
		Config.settings.set_option('Settings', 'ui_account_box_icon_size', '40')
	if not Config.settings.has_option('Settings', 'ui_account_box_icon'):
		Config.settings.set_option('Settings', 'ui_account_box_icon', '')
	if not Config.settings.has_option('Settings', 'ui_log_entry_toggles'):
		Config.settings.set_option('Settings', 'ui_log_entry_toggles', 'system,hats,weapons,tools,crates')
	if not Config.settings.has_option('Settings', 'log_poll_time') or Config.settings.get_option('Settings', 'log_poll_time') == '':
		Config.settings.set_option('Settings', 'log_poll_time', '5')
	if not Config.settings.has_option('Settings', 'ui_log_background_colour') or Config.settings.get_option('Settings', 'ui_log_background_colour') == '':
		Config.settings.set_option('Settings', 'ui_log_background_colour', '000000')
	if not Config.settings.has_option('Settings', 'ui_log_font_colour') or Config.settings.get_option('Settings', 'ui_log_font_colour') == '':
		Config.settings.set_option('Settings', 'ui_log_font_colour', 'FFFFFF')
	if not Config.settings.has_option('Settings', 'ui_log_font_size') or Config.settings.get_option('Settings', 'ui_log_font_size') == '':
		Config.settings.set_option('Settings', 'ui_log_font_size', '10')
	if not Config.settings.has_option('Settings', 'ui_log_font_family') or Config.settings.get_option('Settings', 'ui_log_font_family') == '':
		Config.settings.set_option('Settings', 'ui_log_font_family', 'TF2 Build')
	if not Config.settings.has_option('Settings', 'ui_log_font_style') or Config.settings.get_option('Settings', 'ui_log_font_style') == '':
		Config.settings.set_option('Settings', 'ui_log_font_style', '0')
	if not Config.settings.has_option('Settings', 'ui_log_font_weight') or Config.settings.get_option('Settings', 'ui_log_font_weight') == '':
		Config.settings.set_option('Settings', 'ui_log_font_weight', '50')
	if not Config.settings.has_option('Settings', 'ui_log_font_strikeout') or Config.settings.get_option('Settings', 'ui_log_font_strikeout') == '':
		Config.settings.set_option('Settings', 'ui_log_font_strikeout', 'False')
	if not Config.settings.has_option('Settings', 'ui_log_font_underline') or Config.settings.get_option('Settings', 'ui_log_font_underline') == '':
		Config.settings.set_option('Settings', 'ui_log_font_underline', 'False')
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