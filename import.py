import os, sys
import Config
from TF2IdleConfig import config

optionsfile = 'tf2idle.ini'
		
if __name__ == "__main__":
	Config.init(optionsfile)
	if not os.path.exists(optionsfile):
		print 'Create the .ini file first'
		sys.exit()
	else:
		for account in config['IdleAccounts']:
			if not Config.settings.has_section('Account-' + account['username']):
				Config.settings.add_section('Account-' + account['username'])
				Config.settings.set_option('Account-' + account['username'], 'steam_username', account['username'])
				Config.settings.set_option('Account-' + account['username'], 'steam_username', account['username'])
				Config.settings.set_option('Account-' + account['username'], 'steam_password', account['password'])
				Config.settings.set_option('Account-' + account['username'], 'steam_vanityid', account['steamID'])
				if account.has_key('displayname'):
					Config.settings.set_option('Account-' + account['username'], 'account_nickname', account['displayname'])
				else:
					Config.settings.set_option('Account-' + account['username'], 'account_nickname', '')
				if account.has_key('sandboxname'):
					Config.settings.set_option('Account-' + account['username'], 'sandbox_name', account['sandboxname'])
				else:
					Config.settings.set_option('Account-' + account['username'], 'sandbox_name', '')
				if account.has_key('steaminstall'):
					Config.settings.set_option('Account-' + account['username'], 'sandbox_install', account['steaminstall'])
				else:
					Config.settings.set_option('Account-' + account['username'], 'sandbox_install', '')
				if account.has_key('group'):
					groupstring = ''
					for group in account['group']:
						groupstring += group + ','
					groupstring = groupstring[:-1]
					Config.settings.set_option('Account-' + account['username'], 'groups', groupstring)
				else:
					Config.settings.set_option('Account-' + account['username'], 'groups', '')
		Config.settings.flush_configuration()