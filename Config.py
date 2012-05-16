import ConfigParser
from cStringIO import StringIO
from Encrypt import AESObject

class _settings(ConfigParser.RawConfigParser):
	""" Easy option getting/setting """
	def __init__(self, filename, encryption_key):
		self._parser = ConfigParser.RawConfigParser()
		self.filename = filename
		self.encryption_key = encryption_key

		try:
			if self.encryption_key:
				self.cipher = AESObject(self.encryption_key)
				decrypted_string = self.cipher.decrypt(open(self.filename, 'rb').read())
				f = StringIO(decrypted_string)
				self._parser.readfp(f)
				self.encryption = True
			else:
				self._parser.read(self.filename)
				self.encryption = False
			self.success = True
		except:
			self.success = False

	def returnReadState(self):
		return self.success

	def set_encryption(self, bool):
		self.encryption = bool

	def get_encryption(self):
		return self.encryption

	def set_encryption_key(self, key):
		self.encryption_key = key
		self.cipher = AESObject(self.encryption_key)

	def get_encryption_key(self):
		if self.encryption_key:
			return self.encryption_key
		else:
			return ''

	def has_section(self, sectionname):
		return self._parser.has_section(sectionname)

	def add_section(self, section):
		self._parser.add_section(section)

	def remove_section(self, section):
		self._parser.remove_section(section)
		
	def get_sections(self):
		return self._parser.sections()
		
	def get_option(self, section, opt):
		return self._parser.get(section, opt)

	def set_option(self, section, opt, value = None):
		return self._parser.set(section, opt, value)
		
	def has_option(self, section, opt):
		return self._parser.has_option(section, opt)

	def flush_configuration(self):
		if self.encryption:
			f = StringIO()
			self._parser.write(f)
			encrypted_string = self.cipher.encrypt(f.getvalue())
			open(self.filename, 'wb').write(encrypted_string)
		else:
			self._parser.write(open(self.filename, 'wb'))

	def __setitem__(self, key, value):
		return self.set_option(key, value)

	def __getitem__(self, key):
		try:
			return self.get_option(key)
		except ConfigParser.NoOptionError as E:
			raise KeyError(E)

	def __contains__(self, section, item):
		return self._parser.has_option(section, item)

settings = None
def init(filename, encryption_key=None):
	global settings
	settings = _settings(filename, encryption_key)
