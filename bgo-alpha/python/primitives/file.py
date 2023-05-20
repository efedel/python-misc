#!/usr/bin/python
'''
	Base File class
'''

import sys 
import md5
import os.path
import array
# -- bgo --
import utils.set as set

class File(object):
	# File types. The IDs are from the DB schema
	TYPE_UNK = ("unknown", 1)
	TYPE_EXEC = ("executable", 2)
	TYPE_SO = ("shared library", 3)
	TYPE_AR = ("static library", 4)
	TYPE_OBJ = ("linkable object", 5)
	TYPE_DATA = ("data", 6)
	
	FORMAT_UNK = ("Unknown", 1)
	
	ARCH_UNK = ("Unknown", 1)
	# recognized cpu architectures; file format modules can
	# provide more. Once again, IDs are DB defaults
	ARCH_X86 = ("x86", 2)
	ARCH_X8664 = ("x86-64", 3)
	ARCH_SPARC = ("SPARC", 4)
	ARCH_PPC = ("PPC", 5)
	ARCH_ARM = ("ARM", 6)
	ARCH_JVM = ("JVM", 7)
	ARCH_CLI = ("CLR", 8)
	ARCH_IA64 = ("IA64", 9)
	
	OS_UNK = ("Unknown", 1)
	# recognized operating systems. db defaults, can be extended.
	OS_LINUX = ("Linux", 2)
	OS_FREEBSD = ("FreeBSD", 3)
	OS_OPENBSD = ("OpenBSD", 4)
	OS_NETBSD = ("NetBSD", 5)
	OS_SOLARIS = ("Solaris", 6)
	OS_OSX = ("OS/X", 7)
	OS_DOS = ("DOS", 8)
	OS_WIN = ("Win16", 9)
	OS_WIN32 = ("Win9x", 10)
	OS_WINNT = ("WinNT/2K/XP", 11)
	
	def __init__(self, path=None, ident=None):
		if path == None:
			self._name = ""
			self._path = ""
			raise RuntimeWarning, \
				"Attempt to create File with empty path"
		else:
			self._path = path
			self._name = os.path.basename(path)
		
		# file ident returned by magic
		self._ident = ident
		if self._ident == None:
			self._ident = ""
		
		# binary image: all bytes in file
		self._image = None
		self._size = 0
		self._md5 = None
			
		# file type, e.g. library, executable, data
		self._type = self.TYPE_UNK
		# file format name , e.g. ELF, PE or OMF
		self._format = self.FORMAT_UNK
		self._arch = self.ARCH_UNK
		self._os = self.OS_UNK
			
		# set of all sections in file
		self._sections = set.Set( get_key = lambda s: s._name )
		# set of all instructions in file
		self._insn = set.Set( get_key = lambda i: i._address )
		# set of all data items in file
		self._data = set.Set( get_key = lambda d: d._address )
		# set of all symbols in file
		self._symbols = set.Set( get_key = lambda s: s._name )
		# set of all strings in file
		self._strings = set.Set( get_key = lambda s: s._address )
		# set of all entry points -- use symbols for this?
		self._entry = []
			
		# File object containing this one
		self._container = None
		# Code layers (see DB spec)
		self._layers = [ { 'name':'Orig', 'db_id' : 0 } ]
			
		# info in the file header supplied by compiler vendor
		self._vendor_data = {}
		
		# hash for storing user-provided comments etc
		# this is meant to be public: its contents are user-defined
		self.user_data = {}

		# These are called in subclasses -- not all files want
		# to be loaded and parsed! currently BGObjFile does though.
		# self.load()
		# self.parse()

		
	# File API
	# - Actions
	def load(self, path=None):
		'''
		Load bytes in file into File._image
		'''
		if path != None:
			self._path = path
		if self._path == None:
			raise ValueError, "Attempt to load file 'None'"
		
		try:
			f = file( self._path, 'rb' )
		except IOError, e:
			sys.stderr.write("Unable to open " + self._path + \
			                 " " + str(e))
			raise e
		
		# seek to end to get size
		f.seek(0, 2)
		self._size = f.tell
		
		# load file into self._image
		f.seek(0, 0) 
		try:
			self._image = f.read()
			f.close()
		except IOError, e:
			sys.stderr.write("Error reading " + self._path + \
			                 " " + str(e))
			raise e
		
		if len(self._image) < self._size:
			self._size = len(self._image)
		
		# Generate md5 checksum for file
		md5sum = md5.new()
		md5sum.update(self._image)
		self._md5 = md5sum.digest()

	def parse(self):
		'''
		Parse loaded File
		'''
		raise TypeError, 'File: parse() method is virtual'

	def add_section(self, section):
		self._sections.add(section)

	def add_insn(self, insn):
		self._insn.add(insn)

	def add_data(self, data):
		self._data.add(data)

	def add_symbol(self, sym):
		self._symbols.add(sym)

	def add_string(self, str):
		self._strings.add(str)

	def add_entry(self, addr):
		self._entry.append(addr)

	def add_layer(self, name):
		self._layers.append( { 'name' : name, 'db_id' : 0 } )


	# iterator for sections
	def sections(self):
		'''
		Return iterator for File._sections
		'''
		return self._sections.__iter__()

	# iterator for data addresses
	def data(self):
		'''
		Return iterator for File._data
		'''
		return self._data.__iter__()

	# iterator for symbols
	def symbols(self):
		'''
		Return iterator for File._symbols
		'''
		return self._symbols.__iter__()

	# iterator for strings
	def strings(self):
		'''
		Return iterator for File._strings
		'''
		return self._strings.__iter__()

	# quasi-iterator for bytes in image
	def bytes(self):
		'''
		Return iterator for File._image
		'''
		return self._image.__iter__()

	def size(self):
		'''
		Return size of File in bytes
		'''
		return self._size

	def md5(self):
		'''
		Return the MD5 checksum of File
		'''
		return self._md5

	def ident(self):
		'''
		Return results of file(1) for File
		'''
		return self._ident

	def type(self):
		'''
		Return File type (executable, library, etc)
		'''
		return self._type[0]

	def format(self):
		'''
		Return File format name
		'''
		return self._format[0]
	
	def arch(self):
		return self._arch[0]
	
	def os(self):
		return self._os[0]

	def name(self):
		'''
		Return name of File
		'''
		return self._name

	def path(self):
		'''
		Return full path to File
		'''
		return self._path

	def read(self, offset=0, length=None):
		'''
		Read bytes from File._image and return as a string.
		'''
		if length == None or length > self._size:
			# default to entire file
			length = self._size - offset
		
		# read length bytes from self._image[offset]
		return self._image[offset:offset+length]
	
	def read_bytearray(self, offset=0, length=None):
		'''
		Read bytes from File._image and return as
		an array of bytes, suitable for disassembly
		'''
		buf = self.read(offset, length)
		return array.array('B', buf)

	def write(self, offset, buffer):
		'''
		Write bytes to File._image
		'''
		# write buffer to self._image[offset]
		# does python provide any way to do this aside from
		#  self._image = self._image[0:offset] + buffer + \
		#                self_image[len(buffer):]
		# ?
		# self.autosave()
		pass

	def export(self, path=None):
		'''
		Write bytes in File._image to file
		'''
		# save self._image to disk
		if path == None:
			path = self._path
		
		try:
			f = file(path, 'w')
			f.write(self._image)
			f.close()
		except IOError, e:
			raise e

	def __hash__(self):
		pass

	def __eq__(self, file):
		return self._md5 == file._md5

	def __cmp__(self, file):
		return self._md5 == file._md5

	# misc niceties
	def __str__(self):
		# TODO : XML
		# foreach section...
		return 'File: ' + self.name() + ' @ ' + self.path() + \
			" (" + self.format() + " " + self.type() + "): " + \
			self.ident()
