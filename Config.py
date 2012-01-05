import ConfigParser, os, sys

class settings(ConfigParser.SafeConfigParser):
	""" Easy option getting/setting """
	def __init__(self, filename):
		self._parser = ConfigParser.SafeConfigParser()

		self.filename = filename

		self._parser.read(self.filename)
		
	def has_section(self, sectionname):
		return self._parser.has_section(sectionname)
	
	def set_section(self, sectionname):
		self.sectionname = sectionname

	def add_section(self):
		try:
			self._parser.add_section(self.sectionname)
		except ConfigParser.DuplicateSectionError:
			return None
		
	def get_option(self, opt):
		return self._parser.get(self.sectionname, opt)

	def set_option(self, opt, value = None):
		return self._parser.set(self.sectionname, opt, value)

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

	def __contains__(self, item):
		return self._parser.has_option(self.sectionname, item)