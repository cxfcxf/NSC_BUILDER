import os
import os.path as path
import re
import sys
from binascii import hexlify as hx, unhexlify as uhx
from pathlib import Path

def _exe_dir():
	if getattr(sys, 'frozen', False):
		return Path(os.path.dirname(sys.executable))
	return Path('.')

my_file = Path('keys.txt')
my_file2 = Path('ztools\\keys.txt')
my_file3 = _exe_dir() / 'keys.txt'
my_file4 = Path('prod.keys')
my_file5 = _exe_dir() / 'prod.keys'

class Keys(dict):
	def __init__(self, keys_type):
		self.keys_type = keys_type
		is_key  = re.compile(r'''\s*([a-zA-Z0-9_]*)\s* # name
								=
								\s*([a-fA-F0-9]*)\s* # key''', re.X)
		f = None
		try:
			if my_file.is_file():
				f = open('keys.txt', 'r')
			elif my_file4.is_file():
				f = open('prod.keys', 'r')
			elif my_file2.is_file():
				f = open('ztools\\keys.txt', 'r')
			elif my_file3.is_file():
				f = open(str(my_file3), 'r')
			elif my_file5.is_file():
				f = open(str(my_file5), 'r')
		except FileNotFoundError:
			pass
		if f is None:
			try:
				f = open(path.join(path.dirname(path.abspath(__file__)), '%s' % self.keys_type), 'r')
			except FileNotFoundError:
				raise FileNotFoundError('Need key file %s.keys in either %s or %s' % (self.keys_type,
					path.expanduser('~/.switch'), path.dirname(path.abspath(__file__))))
		iterator = (re.search(is_key, l) for l in f)
		super(Keys, self).__init__({r[1]: uhx(r[2]) for r in iterator if r is not None})
		f.close()

	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			raise KeyError('Missing key %s in %s' % (item, self.keys_type))

class ProdKeys(Keys):
	def __init__(self):
		super(ProdKeys, self).__init__('keys.txt')
		if 'header_key' in self:
			self['nca_header_key'] = self.pop('header_key')

class DevKeys(Keys):
	def __init__(self):
		super(DevKeys, self).__init__('dev')

class TitleKeys(Keys):
	def __init__(self):
		super(TitleKeys, self).__init__('title')
		if 'header_key' in self:
			self['nca_header_key'] = self.pop('header_key')
