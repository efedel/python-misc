#!/usr/bin/python
'''
	Big O Disassembly Buffer class
'''

import array
import types
# --bgo-- 
import utils.set as set

class DisasmBuffer(object):
	def __init__(self, bytes, rva=0, file_offset=0, insn_set=None):
		'''
			bytes : python string of bytes available for disassembly
			rva : load address of bytes[0]
			insn_set : set of instruction objects; stores the
				disassembled insns on output, and is used
				to determine if an address has already
				been disassembled.
		'''
		self._image = bytes
		self._size = len(bytes)
		self._bytes = array.array('B', bytes)
		self._load_addr = rva
		self._offset = file_offset,
		self._insn = insn_set
		if self._insn is None:
			self._insn = set.Set( lambda i: i._address )
	
	def __getitem__(self, item):
		arr = self.bytes()
		if isinstance(item, types.SliceType):
			tmp = arr[item.start:item.stop]
			return tmp.tolist()
		return [arr[item]]
	
	def load_addr(self):
		return self._load_addr

	def size(self):
		'''
		   return length of buffer in bytes
		'''
		return self._size

	def image(self):
		'''
		   return buffer as a string of bytes
		'''
		return self._image
	
	def bytes(self):
		'''
		   return buffer as array of unsigned bytes
		'''
		return self._bytes
	
	def instructions(self):
		'''
		   return iterator over instructions
		'''
		return self._insn
	
	def add_insn(self, insn):
		self._insn.add(insn)

	def seen_address(self, addr):
		class i:
			def __init__(self, addr):
				self._address = addr
		insn = i(addr)
		return self._insn.contains(insn)

	def rva_to_offset(self, rva):
		'''
		   calculate the offset into buffer of an rva
		'''
		if rva < self._load_addr or \
			rva > self._load_addr + self._size:
			raise AssertionError, 'RVA exceeds bounds'
		
		return rva - self._load_addr

	def offset_to_rva(self, offset):
		'''
		   calculate the rva of an offset into the buffer
		'''
		if offset < 0 or offset > self._size:
			raise AssertionError, 'RVA exceeds bounds'
		
		return self._load_addr + offset

	def offset_to_file_offset(self, offset):
		if offset < 0 or offset > self._size:
			raise AssertionError, 'RVA exceeds bounds'
		return self._offset + offset

	def rva_to_file_offset(self, rva):
		if rva < self._load_addr or \
			rva > self._load_addr + self._size:
			raise AssertionError, 'RVA exceeds bounds'
		return self._offset + (rva - self._load_addr)

	#def __str__(self):
	#def __repr__(self):

class DisasmStdout(DisasmBuffer):
	'''
		Example of a DisasmBuffer: this stores the address of each
		instruction it disassembles, then prints the repr() of the 
		instruction to stdout
	'''

	def __init__(self, bytes, rva=0, file_offset=0, insn_set=None):
		self._image = bytes
		self._size = len(bytes)
		self._bytes = array.array('B', bytes)
		self._load_addr = rva
		self._offset = file_offset
		self._addr_seen = {}

	def instructions(self):
		'''
		   return iterator over instructions
		'''
		return iter( () )
	
	def add_insn(self, insn):
		self._addr_seen[insn.address()] = True
		print repr(insn)

	def seen_address(self, addr):
		return addr in self._addr_seen
