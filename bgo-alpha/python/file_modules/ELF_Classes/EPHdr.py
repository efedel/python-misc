#!/usr/bin/python
'''
	Big O ELF File module : EPHdr
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

class ElfSegment(object):
	_format = 'IIIIIIII'
	type_strings = ( 'Null', 'Load', 'Dynamic', 'Interp', 'Note', 'Shlib',
	                 'Phdr', 'TLS' )
	flag_strings = { 1 : 'X', 2 : 'W', 3 : 'R' }
	note_core_strings = { 1: 'PRStatus', 2:'FPRegSet', 3:'PRPSInfo',
			      4:'TaskStruct', 5:'Platform', 6:'AuxV',
			      7:'GWindows', 8:'ASRS', 10:'PStatus', 
			      13:'PSInfo', 14:'PRCred', 15:'UTSName',
			      16:'LWPStatus', 17:'LWPSInfo', 20:'PRFPXReg' }
	note_obj_strings = ( 'None', 'Version' )

	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
			if len(buf) < size:
				raise AssertionError, 'Buf size ' + \
				      str(len(buf)) + "\n"
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			phdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.type_raw = phdr[0]
		try:
			self.type = self.type_strings[phdr[0]]
		except IndexError, e:
			self.type = 'Invalid type: ' + hex(phdr[0])
		
		self.offset = phdr[1]
		self.vaddr = phdr[2]
		self.paddr = phdr[3]
		self.file_size = phdr[4]
		self.mem_size = phdr[5]
		self.flags_raw = phdr[6]
		
		self.flags = ''
		for i in self.flag_strings.iterkeys():
			if self.flags_raw & i:
				if len(self.flags):
					self.flags += '|'
				self.flags += self.flag_strings[i]
		
		self.align = phdr[7]

	def __str__(self):
		return  'Type: ' + self.type + \
			"\tFlags: " + self.flags + "\n" + \
			'Offset: ' + hex(self.offset) + \
			"\tVirtual Address: " + hex(self.vaddr) + \
			"\tPhysical Address: " + hex(self.paddr) + "\n" + \
			"File Size: " + str(self.file_size) + \
			"\tMemory Size: " + str(self.mem_size) + \
			"\tAlignment: " + str(self.align) + "\n"

class ElfSegment32(ElfSegment):
	_format = 'IIIIIIII'
	def __init__(self, file, offset):
		ElfSegment.__init__(self, file, offset)

class ElfSegment64(ElfSegment):
	_format = 'IIQQQQQQ'
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
			if len(buf) < size:
				raise AssertionError, 'Buf size ' + \
				      str(len(buf)) + "\n"
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			phdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.type_raw = phdr[0]
		try:
			self.type = self.type_strings[phdr[0]]
		except IndexError, e:
			self.type = 'Invalid version: ' + hex(phdr[0])
		
		self.flags_raw = phdr[1]
		self.flags = ''
		for i in self.flag_strings.iterkeys():
			if self.flags_raw & i:
				if len(self.flags):
					self.flags += '|'
				self.flags += self.flag_strings[i]
		
		self.offset = phdr[2]
		self.vaddr = phdr[3]
		self.paddr = phdr[4]
		self.file_size = phdr[5]
		self.mem_size = phdr[6]
		self.align = phdr[7]

