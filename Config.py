import ConfigParser, os, sys

class _settings(ConfigParser.SafeConfigParser):
	""" Easy option getting/setting """
	def __init__(self, filename):
		self._parser = ConfigParser.SafeConfigParser()

		self.filename = filename
		try:
			self._parser.read(self.filename)
		except:
			pass
		
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
		return  self._parser.has_option(section, opt)

	def flush_configuration(self):
		self._parser.write(open(self.filename, "w"))

	def __del__(self):
		self.flush_configuration()

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
def init(filename):
	global settings
	settings = _settings(filename)
