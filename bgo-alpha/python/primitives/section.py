#!/usr/bin/python
'''
	Base File Section Class
'''

# --bgo--
import utils.set as set
import disasmbuf
import BGDisasmFactory

class Section(disasmbuf.DisasmBuffer):
	# Section types. The IDs are from the DB schema.
	# NOTE: filehdr doubles as 'unknown'
	FILEHDR  = ("Header", 1) # File format bookeeping info
	PROGCODE = ("Code", 2) # Program Executable Code
	PROGDATA = ("Data", 3) # Program Readable(/Writeable) Data
	RESOURCE = ("Resource", 4) # Resource or embedded UI data
	DEBUG = ("Debug", 5) # definition of toolchain symbols
	
	# NOTE: java const pool field, attr, ifaces all symbols 
	SYMBOL = ("Symbol", 6) # definition of global symbols
	IMPORT = ("Import", 7) # definition of imported code/data addr
	EXPORT = ("Export", 8) # defintion of exported code/data addr
	RELOC = ("Reloc", 9) # Internal addresses needing dynamic reloc
	NOTE = ("Note", 10) # Advisory info provided by author/toolchain
	section_types = (FILEHDR, PROGCODE, PROGDATA, RESOURCE,
					 DEBUG, SYMBOL, IMPORT, EXPORT, RELOC, 
					 NOTE)
	
	# compiler type
	COMPILER_UNK = ( 'Unknown', 1 );
	COMPILER_GCC = ( 'gcc', 2 );
	COMPILER_SUN = ( 'Sun CC', 3 );
	COMPILER_MS = ( 'Visual C++', 4 );
	# source lang
	LANG_ASM = ( 'Assembler', 1 );
	LANG_C = ( 'C', 2 );
	LAN_CPP = ( 'C++', 3 );
	LANG_CSHARP = ( 'C#', 4 );
	LANG_JAVA = ( 'JAVA', 5 );
	LANG_FORTRAN = ( 'FORTRAN', 6 );

	# Section Flags
	NOINIT = "Unitialized" # Uninitialized Data
	ALLOC = "Allocated" # Not allocated
	section_flags = (NOINIT, ALLOC)

	# Section Permissions
	ACCESS_R  = 0x01   
	ACCESS_W = 0x02
	ACCESS_X  = 0x04	

	#def __doc__(self):
	#__slots__
	ENDIAN_BIG = 'big'
	ENDIAN_LITTLE = 'little'
	
	def __init__(self, file, name, offset=0, size=0, load_addr=0,
				 endian=ENDIAN_BIG, word_size=1, arch=None):
		self._name = name
		self._size = size
		self._offset = offset
		self._type = self.FILEHDR
		self._access = 0
		self._flags = []
		# disasmbuf api
		# _bytes and _image are accessed only by method
		self._load_addr = load_addr
		self._insn = file._insn.subset()		
		# bad! tight coupling!
		# but it makes subsets work
		# need a more elegant interface...
		# perhap set these in file via add_section? 
		self._data = file._data.subset()
		self._symbols = file._symbols.subset()
		self._strings = file._strings.subset()
		if file is None:
			raise AssertionError, \
				'Attempt to create a section outside of a File'
		self._file = file
		
		# cpu arch of code in section, if applicable
		# ok, there should be a codesection subclass :P
		if arch is None:
			arch = file._arch
		self._arch = arch
		# data endianness
		self._endian = endian
		# cpu word size
		self._word_size = word_size
		# compiler type
		self._compiler = self.COMPILER_UNK
		# source language type
		self._lang = self.LANG_ASM
		
		
		# set of insructions
		# user_data is intended for use only by the caller
		self.user_data = {}

	# DisasmBuffer Interface
	def image(self):
		return self._file.read(self._offset, self._size)

	def bytes(self):
		return self._file.read_bytearray(self._offset, self._size)

	def instructions(self):
		''' return iterator over code addresses '''
		return self._insn

	def add_insn(self, insn):
		''' add insn object to section '''
		if insn is None:
			raise TypeError, 'Invalid instruction: None'
		self._insn.add(insn)

	# Section Interface
	# - Actions
	def disassemble(self):
		if self._arch is None:
			raise AttributeError, 'No cpu defined for section' 
		
		# load appropriate disassembler module
		# TODO: some global prefs for disassembler?
		#       maybe make disassembler a singleton?
		disasm = BGDisasmFactory.DisasmFactory(self.arch())
		
		# foreach symbol, disasm forward
		for s in self._symbols:
			offset = self.rva_to_offset(s.load_address)
			disasm.disasm_forward(self, offset)
		
		# linear disasm from start of section
		disasm.disasm_range(self)

	# - Alter section metadata
	def rename(self, str):
		if str is None:
			raise TypeError, 'Invalid string: None'
		self._name = str

	def set_flag(self, str):
		if str is None:
			raise TypeError, 'Invalid string: None'
		if str not in self.section_flags:
			raise ValueError, 'Invalid section flag ' + str
		if str not in self._flags:
			self._flags.append(str)

	def clear_flag(self, str):
		if str is None:
			raise TypeError, 'Invalid string: None'
		if str in self._flags:
			self._flags.remove(str)

	#  - Access section metadata
	def file(self):
		''' return file object owning section '''
		return self._file
	
	def name(self):
		''' return section name : string '''
		return self._name

	def offset(self):
		''' return section file offset : unsigned int '''
		return self._offset

	def size(self):
		''' return section size, in bytes : unsigned int '''
		return self._size

	def load_addr(self):
		''' return section load address(rva) : unsigned int '''
		return self._load_addr

	def type(self, str=None):
		''' return section type : string '''
		return self._type[0]

	def flags(self, lst=None):
		''' return section flags : list of strings '''
		return self._flags

	def flags_str(self):
		''' return section flags: string '''
		flags = None
		
		for f in self._flags:
			if flags is not None:
				flags = flags + '|' + f
			else:
				flags = f
		
		if flags is None:
			flags = ''
		
		return flags

	def access(self):
		''' return section access perms : integer '''
		return self._access
	
	def access_str(self):
		''' return section access perms : string '''
		# python strings cannot be assigned. why guido why???
		perm = ['-','-','-']
		if self._access & self.ACCESS_R:
			perm[0] = 'r'
		if self._access & self.ACCESS_W:
			perm[1] = 'w'
		if self._access & self.ACCESS_X:
			perm[2] = 'x'
		return perm[0] + perm[1] + perm[2]
	
	def arch(self):
		''' return cpu/disasm name for section: string '''
		return self._arch[0]
	
	def word_size(self):
		''' return machine word size for section : integer '''
		return self._word_size
	
	def endian(self):
		''' return endianness of section : string '''
		return self._endian

	def compiler(self):
		''' return compiler used to generate section '''
		return self._compiler[0]
	
	def source_lang(self):
		''' return source language of section '''
		return self._lang[0]

	# Add section contents
	def add_data(self, data):
		''' add data object to section '''
		if data is None:
			raise TypeError, 'Invalid data: None'
		self._data.add(data)

	def add_symbol(self, sym):
		''' add symbol object to section '''
		if sym is None:
			raise TypeError, 'Invalid symbol: None'
		self._symbols.add(sym)

	# - Access section contents
	def data(self):
		''' return terator over data addresses '''
		return iter(self._data)

	def symbols(self):
		''' return iterator over symbols '''
		return iter(self._symbols)

	# - Class behavior
#	def __contains__(self, insn):
#		return insn in self._insn

#		''' primary key : offset '''
#		pass

#	def __cmp__(self, insn):
#		pass

	def __str__(self):
		return "Name: " + self.name() + \
		       "\tType: " + self.type() + "\n" \
		       "Offset: " + hex(self.offset()) + \
		       "\tSize: " + hex(self.size()) + \
		       "\tLoad Address: " + hex(self.load_addr()) + "\n"

	#def __iter__(self):
	#	return iterator over code/data? or buffer of bytes?
	#def __len(self):
	#	return size of structure?




