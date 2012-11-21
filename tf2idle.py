import sys, logging
from PyQt4 import QtCore, QtGui

import Config
from MainWindow import MainWindow
from Common import returnResourcePath

optionsfile = 'tf2idle.ini'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('tf2idle_exceptions.txt', delay=True))

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
		Config.settings.set_option('Settings', 'backpack_viewer', 'Steam')
	if not Config.settings.has_option('Settings', 'launch_options'):
		Config.settings.set_option('Settings', 'launch_options', '+exec idle.cfg -textmode -nosound -low -novid -nopreload -nojoy -sw +sv_lan 1 -width 640 -height 480 +map itemtest')
	if not Config.settings.has_option('Settings', 'launch_delay_time') or Config.settings.get_option('Settings', 'launch_delay_time') == '':
		Config.settings.set_option('Settings', 'launch_delay_time', '0')
	if not Config.settings.has_option('Settings', 'log_file_formatting'):
		Config.settings.set_option('Settings', 'log_file_formatting', '{date}, {time}, {itemtype}, {item}, {id}, {account}{nline}')
	if not Config.settings.has_option('Settings', 'easy_sandbox_mode') or Config.settings.get_option('Settings', 'easy_sandbox_mode') == '':
		Config.settings.set_option('Settings', 'easy_sandbox_mode', 'no')
	if not Config.settings.has_option('Settings', 'sys_tray_notifications'):
		Config.settings.set_option('Settings', 'sys_tray_notifications', 'hats,tools')
	if not Config.settings.has_option('Settings', 'close_to_tray') or Config.settings.get_option('Settings', 'close_to_tray') == '':
		Config.settings.set_option('Settings', 'close_to_tray', 'False')
	if not Config.settings.has_option('Settings', 'log_web_view') or Config.settings.get_option('Settings', 'log_web_view') == '':
		Config.settings.set_option('Settings', 'log_web_view', 'Off')
	if not Config.settings.has_option('Settings', 'log_web_view_port') or Config.settings.get_option('Settings', 'log_web_view_port') == '':
		Config.settings.set_option('Settings', 'log_web_view_port', '5000')
	
	if not Config.settings.has_option('Settings', 'ui_no_of_columns') or Config.settings.get_option('Settings', 'ui_no_of_columns') == '':
		Config.settings.set_option('Settings', 'ui_no_of_columns', '2')
	if not Config.settings.has_option('Settings', 'ui_window_size') or Config.settings.get_option('Settings', 'ui_window_size') == '':
		Config.settings.set_option('Settings', 'ui_window_size', '(890, 600)')
	if not Config.settings.has_option('Settings', 'ui_account_box_font_size') or Config.settings.get_option('Settings', 'ui_account_box_font_size') == '':
		Config.settings.set_option('Settings', 'ui_account_box_font_size', '12')
	if not Config.settings.has_option('Settings', 'ui_account_box_icon_size') or Config.settings.get_option('Settings', 'ui_account_box_icon_size') == '':
		Config.settings.set_option('Settings', 'ui_account_box_icon_size', '40')
	if not Config.settings.has_option('Settings', 'ui_account_box_icon'):
		Config.settings.set_option('Settings', 'ui_account_box_icon', '')
	if not Config.settings.has_option('Settings', 'ui_log_entry_toggles'):
		Config.settings.set_option('Settings', 'ui_log_entry_toggles', 'system,hats,weapons,tools,crates')
	if not Config.settings.has_option('Settings', 'log_poll_time') or Config.settings.get_option('Settings', 'log_poll_time') == '':
		Config.settings.set_option('Settings', 'log_poll_time', '1')
	if not Config.settings.has_option('Settings', 'ui_log_background_colour') or Config.settings.get_option('Settings', 'ui_log_background_colour') == '':
		Config.settings.set_option('Settings', 'ui_log_background_colour', '000000')
	if not Config.settings.has_option('Settings', 'ui_log_font_colour') or Config.settings.get_option('Settings', 'ui_log_font_colour') == '':
		Config.settings.set_option('Settings', 'ui_log_font_colour', 'FFFFFF')
	if not Config.settings.has_option('Settings', 'ui_log_font_size') or Config.settings.get_option('Settings', 'ui_log_font_size') == '':
		Config.settings.set_option('Settings', 'ui_log_font_size', '12')
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

class KeyDialog(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self, None)

		self.setWindowIcon(QtGui.QIcon(returnResourcePath('images/tf2idle.png')))
		self.setWindowTitle('Enter key to continue')
		self.gridLayout = QtGui.QGridLayout(self)
		
		self.textLabel = QtGui.QLabel(self)
		self.textLabel.setText('Enter your decryption key:')
		self.gridLayout.addWidget(self.textLabel, 0, 0, 1, 1)
		
		self.textLineEdit = QtGui.QLineEdit(self)
		self.textLineEdit.setMaxLength(32)
		self.gridLayout.addWidget(self.textLineEdit, 0, 1, 1, 1)
		
		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
		self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
		
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)

	def closeEvent(self, event):
		pass

	def accept(self):
		key = str(self.textLineEdit.text()).strip()
		if key:
			Config.init(optionsfile, key)
			self.close()

def startup():
	setDefaultSettings()
	myapp = MainWindow()
	myapp.show()
	app.exec_()
	Config.settings.flush_configuration()

def my_excepthook(type, value, tback):
	logger.error('Uncaught Exception', exc_info=(type, value, tback))
	# Call the default handler
	sys.__excepthook__(type, value, tback) 

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	Config.init(optionsfile)
	sys.excepthook = my_excepthook

	if Config.settings.returnReadState():
		startup()
	# config file is encrypted
	else:
		firstWindow = KeyDialog()
		firstWindow.exec_()
		if Config.settings.returnReadState():
			startup()
		else:
			dialog = QtGui.QDialog()
			dialog.setWindowIcon(QtGui.QIcon(returnResourcePath('images/tf2idle.png')))
			QtGui.QMessageBox.critical(dialog, 'Error', 'Could not decrypt the config file, your key is incorrect')