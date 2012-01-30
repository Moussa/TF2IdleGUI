from Crypto.Cipher import AES
import base64, os

class AESObject():
	def __init__(self, key):
		self.BLOCK_SIZE = 32
		self.PADDING = '*'
		self.key = key + ('x' * (self.BLOCK_SIZE - len(key)))
		self.cipher = AES.new(self.key)
		
		self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING
		
		self.encodeAES = lambda c, s: base64.b64encode(c.encrypt(self.pad(s)))
		self.decodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)
	
	def encrypt(self, string):
		return self.encodeAES(self.cipher, string)

	def decrypt(self, string):
		try:
			return self.decodeAES(self.cipher, string)
		except ValueError:
			# String isn't correct encrypted length
			return None