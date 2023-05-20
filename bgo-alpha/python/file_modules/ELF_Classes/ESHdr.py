#!/usr/bin/python
'''
	Big O ELF File module : ESHdr
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

class ElfSection(object):
	type_strings = { 0:'NULL', 1:'PROGBITS', 2:'SYMTAB', 3:'STRTAB', 
			 4:'RELA', 5:'HASH', 6:'DYNAMIC', 7:'NOTE', 
			 8:'NOBITS', 9:'REL', 10:'SHLIB', 11:'DYNSYM',
			 14:'INIT_ARRAY', 15:'FINI_ARRAY', 16:'PREINIT_ARRAY',
			 17:'GROUP', 18:'SYMTAB_SHNDX',
			 # GNU- and SUN-specific ones 
			 0x6ffffff7:'GNU_LIBLIST',
			 0x6ffffff8:'CHECKSUM',
			 0x6ffffffa:'SUNW_move',
			 0x6ffffffb:'SUNW_COMDAT',
			 0x6ffffffc:'SUNW_syminfo',
			 0x6ffffffd:'GNU_VERSION_DEF',
			 0x6ffffffe:'GNU_VERSION_NEED',
			 0x6fffffff:'GNU_VERSION_SYMTAB'};

	flag_strings = { 1:'WRITE', 2:'ALLOC', 4:'EXECINSTR', 8:'MERGE',
			16:'STRINGS', 32:'INFO_LINK', 64:'LINK_ORDER',
			128:'OS_NONCONFORMING', 256:'GROUP', 512:'TLS' }

	# default to 32-bit format
	_format = 'IIIIIIIIII';

	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
			if len(buf) < size:
				raise AssertionError, 'Buf size ' + \
				      str(len(buf)) + ' on read of ' + \
				      str(size) + "\n"
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			shdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.name_raw = shdr[0]
		# self.name is determine when string table is known
		self.name = 'Unknown'
		
		self.type_raw = shdr[1]
		try:
			self.type = self.type_strings[shdr[1]]
		except KeyError, e:
			self.type = 'Invalid type: ' + str(shdr[1])
		
		self.flags_raw = shdr[2]
		self.flags = ''
		for i in self.flag_strings.iterkeys():
			if self.flags_raw & i:
				if len(self.flags):
					self.flags += '|'
				self.flags += self.flag_strings[i]
		
		self.addr = shdr[3]
		self.offset = shdr[4]
		self.size = shdr[5]
		self.link = shdr[6]
		self.info = shdr[7]
		self.addralign = shdr[8]
		self.entsize = shdr[9]

	def __str__(self):
		return  'Name: ' + self.name + \
		        "\tType: " + self.type + \
		        "\tFlags: " + self.flags + "\n" + \
		        'Offset: ' + hex(self.offset) + \
		        "\tAddress: " + hex(self.addr) + \
		        "\tSize: " + str(self.size) + "\n"

class ElfSection32(ElfSection):
	_format = 'IIIIIIIIII';
	def __init__(self, file, offset):
		ElfSection.__init__(self, file, offset)

class ElfSection64(ElfSection):
	_format = 'IIQQQQIIQI';
	def __init__(self, file, offset):
		ElfSection.__init__(self, file, offset)

