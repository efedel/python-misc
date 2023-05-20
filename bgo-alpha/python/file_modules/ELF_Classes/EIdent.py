#!/usr/bin/python
'''
	Big O ELF File module: EIdent
'''

import sys
import struct
sys.path.append(".")
# -- bgo --


class EIdent(object):
	_format = "4sBBBBB7s"
	file_class_strings = ( 'none', '32', '64' )
	data_strings = ( 'None', 'LSB (little endian)', 'MSB (big endian)' )
	os_abi_strings = { 0:'SysV', 1:'HPUX', 2:'NetBSD', 3:'Linux',
	                   6:'Solaris', 7:'AIX', 8:'Irix', 9:'FreeBSD', 
	                   10:'Tru64', 11:'Modesto', 12:'OpenBSD', 97:'ARM',
	                   255:'Standalone' }
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			ident = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.magic = ident[0]
		
		self.file_class_raw = ident[1]
		try:
			self.file_class = self.file_class_strings[ident[1]]
		except IndexError, e:
			self.file_class = 'Invalid file class: ' + str(ident[1])
		
		self.data_raw = ident[2]
		try:
			self.data = self.data_strings[ident[2]]
		except IndexError, e:
			self.data = 'Invalid data: ' + str(ident[2])
		
		self.version = ident[3]
		
		self.os_abi_raw = ident[4]
		try:
			self.os_abi = self.os_abi_strings[ident[4]]
		except KeyError, e:
			self.os_abi = 'Invalid OS ABI: ' + str(ident[4])
		
		self.abi_version = ident[5]
		self.pad = ident[6]

	def __str__(self):
		# TODO: XML
		return 'Magic: ' + self.magic + \
		       "\tClass: " + self.file_class + ' bit' +\
		       "\tData: " + self.data + "\n" + \
		       'Version: ' + str(self.version) + \
		       "\tOS ABI: " + self.os_abi + \
		       "\tABI Version: " + str(self.abi_version) + "\n";


