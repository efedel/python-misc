#!/usr/bin/python
'''
	Big O ELF File module
'''

import sys
import struct
sys.path.append(".")
# -- bgo --
import BGModule
import BGFile as file
import BGObjFile as objfile
import BGSection as section

MODULE_VERSION = 0.1
MODULE_NAME = 'ELF'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


ELF_FILE = 'ELFFile'
ELF_MOD_CLASS = 0

class ELFModule(BGModule.Module):
	def __init__(self):
		BGModule.Module.__init__(self, MODULE_NAME, MODULE_VERSION,
					MODULE_AUTHOR, MODULE_LICENSE)
	
	_classes = { ELF_FILE : 0 }
	
	def new_install(self):
		global ELF_FILE, ELF_MOD_CLASS
		
		id = self.db().insert( 'module_class', 
				{ 'classname' :ELF_FILE,
				  'filename' : 'file_modules.ELF',	
				  'module' : self.db_id() } )
		ELF_MOD_CLASS = id

	def upgrade_install(self, version):
		pass
	

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


# -----------------------------------------------------------------------------
class Ehdr(object):
	# default will be class 32 header for now
	_format = "16sHHIIIIIHHHHHH";
	type_strings = { 0: 'None', 
	                 1: 'Relocatable',
	                 2: 'Executable',
	                 3: 'Shared',
	                 4: 'Core' }
	
	machine_strings = { 0:'None', 
				1:'AT&T WE 32100', 
				2:'SUN SPARC',
				3:'Intel 80386', 
				4:'Motorola m68k family', 
				5:'Motorola m88k family', 
				7:'Intel 80860',
				8:'MIPS R3000 big-endian', 
				9:'IBM System/370', 
				10: 'MIPS R3000 little-endian',
				15: 'HPPA',
				17: 'Fujitsu VPP500',
				18: 'Sun "v8plus"',
				19: 'Intel 80960',
				20: 'PowerPC',
				21: 'PowerPC 64-bit',
				22: 'IBM S390',
			    36: 'NEC V800 series',
			    37: 'Fujitsu FR20',
			    38: 'TRW RH-32',
			    39: 'Motorola RCE',
			    40: 'ARM',
			    41: 'Digital Alpha',
			    42: 'Hitachi SH',
			    43: 'SPARC v9 64-bit',
			    44: 'Siemens Tricore',
			    45: 'Argonaut RISC Core',
			    46: 'Hitachi H8/300',
			    47: 'Hitachi H8/300H',
			    48: 'Hitachi H8S',
			    49: 'Hitachi H8/500',
			    50: 'Intel Merced`',
			    51: 'Stanford MIPS-X',
			    52: 'Motorola Coldfire',
			    53: 'Motorola M68HC12',
			    54: 'Fujitsu MMA Multimedia Accelerator',
			    55: 'Siemens PCP',
			    56: 'Sony nCPU embedded RISC',
			    57: 'Denso NDR1',
			    58: 'Motorola Start*Core',
			    59: 'Toyota ME16',
			    60: 'STMicroelectronic ST100',
			    61: 'Advanced Logic Corp. Tinyj',
			    62: 'AMD x86-64',
			    63: 'Sony DSP',
			    66: 'Siemens FX66',
			    67: 'STMicroelectronics ST9+ 8/16',
			    68: 'STmicroelectronics ST7',
			    69: 'Motorola MC68HC16',
			    70: 'Motorola MC68HC11',
			    71: 'Motorola MC68HC08',
			    72: 'Motorola MC68HC05',
			    73: 'Silicon Graphics SVx',
			    74: 'STMicroelectronics ST19',
			    75: 'Digital VAX',
			    76: 'Axis Communicationa',
			    77: 'Infineon Technologies',
			    78: 'Element 14 64-bit DSP',
			    79: 'LSI Logic 16-bit DSP',
			    80: 'Knuth MMIX',
			    81: 'Harvard University machine-independent obj',
			    82: 'SiTera Prism',
			    83: 'Atmel AVR',
			    84: 'Fujitsu FR30',
			    85: 'Mitsubishi D10V',
			    86: 'Mitsubishi D30V',
			    87: 'NEC v850',
			    88: 'Mitsubishi M32R',
			    89: 'Matsushita MN10300',
			    90: 'Matsushita MN10200',
			    91: 'picoJava',
			    92: 'OpenRISC',
			    93: 'ARC Cores Tangent-A5',
			    94: 'Tensilica Xtensa',
			    95: 'Num' }
	version_strings = ( 'None', 'Current' )

	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			ehdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.ident = ehdr[0]
		
		self.type_raw = ehdr[1]
		try:
			self.type = self.type_strings[ehdr[1]]
		except KeyError, e:
			self.type = 'Invalid type: ' + str(ehdr[1])
		
		self.machine_raw = ehdr[2]
		try:
			self.machine = self.machine_strings[ehdr[2]]
		except KeyError, e:
			self.machine = 'Invalid machine: ' + str(ehdr[2])
		
		self.version_raw = ehdr[3]
		try:
			self.version = self.version_strings[ehdr[3]]
		except IndexError, e:
			self.version = 'Invalid version: ' + str(ehdr[3])
		
		self.entry = ehdr[4]
		self.phoff = ehdr[5]
		self.shoff = ehdr[6]
		self.flags = ehdr[7]
		self.ehsize = ehdr[8]
		self.phentsize = ehdr[9]
		self.phnum = ehdr[10]
		self.shentsize = ehdr[11]
		self.shnum = ehdr[12]
		self.shstrndx = ehdr[13]

	def __str__(self):
		# TODO: XML
		return "Ident: " + self.ident + "\n" + \
			"Type: " + self.type + "\n" + \
			"Machine: " + self.machine + "\n" + \
			"Version: " + self.version + "\n" + \
			"Entry: " + hex(self.entry) + "\n" + \
			"PhOff: " + hex(self.phoff) + "\n" + \
			"ShOff: " + hex(self.shoff) + "\n" + \
			"Flags: " + hex(self.flags) + "\n" + \
			"EhSize: " + str(self.ehsize) + "\n" + \
			"PhEntSize: " + str(self.phentsize) + "\n" + \
			"PhNum: " + str(self.phnum) + "\n" + \
			"ShEntSize: " + str(self.shentsize) + "\n" + \
			"ShNum: " + str(self.shnum) + "\n" + \
			"ShStrNdx: " + str(self.shstrndx) + "\n"

class Ehdr32(Ehdr):
	_format = "16sHHIIIIIHHHHHH";
	def __init__(self, file, offset):
		Ehdr.__init__(self, file, offset)

class Ehdr64(Ehdr):
	_format = "16sHHIQQQIHHHHHH";
	def __init__(self, file, offset):
		Ehdr.__init__(self, file, offset)

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
class ElfSymbol(object):
	_format = 'IIIBBH'
	# bind = info >> 4, info = val & 0xf
	bind_strings = ( 'Local', 'Global', 'Weak' )
	type_strings = ( 'None', 'Object', 'Func', 'Section', 'File', 
	                 'Common', 'TLS' )
	# visibility = other & 0x03
	visibility_strings = ( 'Default', 'Internal', 'Hidden', 'Protected' )

class ElfSymbol32(ElfSymbol):
	_format = 'IIIBBH'

class ElfSymbol64(ElfSymbol):
	_format = 'IBBHQQ'
	
class ElfSymbolInfo(object):
	_format = 'HH'
	boundto_strings = { 0xFFFF : 'Self', 0xFFF3 : 'Parent' }
	flag_strings = { 1 : 'Direct', 2: 'PassThru', 4: 'Copy', 8: 'LazyLoad' }
	version_strings = ( 'None', 'Current' )


# -----------------------------------------------------------------------------
class ElfReloc(object):
	_format = 'II'

class ElfReloc32(ElfReloc):
	_format = 'II'
	# sym = info >> 8, type = info &  0xff

class ElfReloc64(ElfReloc):
	_format = 'QQ'
	# sym = info >> 32, type = info & 0xffffffff

class ElfRelocA32(ElfReloc32):
	_format = 'IIi'

class ElfRelocA64(ElfReloc64):
	_format = 'QQq'

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
class ElfDynamic(object):
	_format = 'lI'

class ElfDynamic32(ElfDynamic):
	_format = 'lI'

class ElfDynamic64(ElfDynamic):
	_format = 'qQ'

# -----------------------------------------------------------------------------
class ELFFile(objfile.ObjFile):
	bg_module = None
	
	#TODO : un-hardcode this [use DB]
	ELF_FORMAT=('ELF', 3)
	
	endian_strings = ( section.Section.ENDIAN_BIG,
				section.Section.ENDIAN_LITTLE,
				section.Section.ENDIAN_BIG)

	# cpu_strings: name of disasm module for cpu
	# key must match Ehdr.machine_strings key
	# these tuples are from File.py and the DB
	cpu_strings = { 
		2:file.File.ARCH_SPARC, 	# SPARC 32-bit
		3:file.File.ARCH_X86,	# IA-32
		4:('68000', 1),	# Motorola 68K
		20:file.File.ARCH_PPC,	# PowerPC 32
		21:file.File.ARCH_PPC,	# PowerPC 64
		40:file.File.ARCH_ARM,	# ARM
		41:('DEC', 1),	# Digital Alpha
		43:file.File.ARCH_SPARC, # SPARC 64-bit
		50:file.File.ARCH_IA64,	# Itanic	
		62:file.File.ARCH_X8664  # AMD 64
	}

	def __init__(self, path=None, ident=None, db_id=None):
		if self.bg_module is None:
			ELFFile.bg_module = ELFModule()
		
		# set defaults, load and parse
		self._format = self.ELF_FORMAT
		self._class_db_id = ELF_MOD_CLASS
		
		objfile.ObjFile.__init__(self, path, ident, db_id)
		
		if db_id is not None:
			# restured from DB
			return
		
		#self.autosave()

	def parse(self):
		# handle ELF ident
		self.elf_ident = EIdent(self, 0)
		#self._type = self.TYPE_EXEC
		
		# handle ELF header
		if self.elf_ident.file_class == '32' :
			self.elf_header = Ehdr32(self, 0)
			self.__word_size = 4
		elif self.elf_ident.file_class == '64' :
			self.elf_header = Ehdr64(self, 0)
			self.__word_size = 8
		else:
			# for now we default to 32-bit, maybe change to error
			# later...
			sys.stderr.write('Warning: Unknown ELF class ' + \
			                  self.elf_ident.file_class + "\n" )
			self.elf_header = Ehdr(self, 0)
			self.__word_size = 4
		
		# note: word size, endian, and cpu are internal
		# to ELFFile; they are passed on to the properties
		# of each appropriate sections.
		self.__endian = self.endian_strings[self.elf_ident.data_raw]
		# set name of disassembler
		try:
			self._arch = \
				self.cpu_strings[self.elf_header.machine_raw]
		except KeyError, e:
			self._arch = file.File.ARCH_UNK
		
		# add elf entry point
		self._entry.append(self.elf_header.entry)
		
		# NOTE: elf sections and segments are different from
		#       bgo sections. all the elf stuff is created first,
		#       and the bgo stuff is created based on that info.
		
		# handle section headers
		self.__section_headers()
		
		# handle program segment headers
		self.__program_headers()
		
		# handle sections
		# handle program segments
		
		# create BigO sections
		self.__create_sections()

	def __get_exec_segment(self):

		for ph in self.__segment_list:
			if ph.type == 'Load' and ph.flags.find('X') != -1:
				return ph
		return None

	def __section_shdr_details(self, sec, shdr):
			# TODO
		sec_type = { 'NULL' : sec.FILEHDR, 
				'PROGBITS': sec.PROGDATA, 
				'SYMTAB': sec.SYMBOL, 
				'STRTAB': sec.RESOURCE, 
				'RELA': sec.RELOC,
				'HASH': sec.FILEHDR,
				'DYNAMIC': sec.FILEHDR,
				'NOTE': sec.NOTE, 
				'NOBITS': sec.PROGDATA,
				'REL': sec.RELOC,
				'SHLIB': sec.FILEHDR,
				'DYNSYM': sec.IMPORT,
				'INIT_ARRAY': sec.FILEHDR,
				'FINI_ARRAY': sec.FILEHDR,
				'PREINIT_ARRAY': sec.FILEHDR,
				'GROUP': sec.FILEHDR,
				'SYMTAB_SHNDX': sec.FILEHDR,
				'GNU_LIBLIST':sec.FILEHDR,
				'CHECKSUM':sec.FILEHDR,
				'SUNW_move':sec.FILEHDR,
				'SUNW_COMDAT':sec.FILEHDR,
				'SUNW_syminfo':sec.FILEHDR,
				'GNU_VERSION_DEF':sec.FILEHDR,
				'GNU_VERSION_NEED':sec.FILEHDR,
				'GNU_VERSION_SYMTAB':sec.FILEHDR,
				'.interp': sec.PROGCODE,
				'.init':sec.PROGCODE,
				'.fini':sec.PROGCODE,
				'.text':sec.PROGCODE,
				'.rodata':sec.PROGDATA,
				'.data':sec.PROGDATA,
				'.bss':sec.PROGDATA,
				'.ctors':sec.PROGCODE,
				'.dtors':sec.PROGCODE };
		
		try:
			type = sec_type[shdr.name]
		except KeyError, e:
			type = None
		try:
			if type == None:
				type = sec_type[shdr.type]
		except KeyError, e:
			type = sec.FILEHDR
		
		for f in shdr.flags.split('|'):
			if f == 'WRITE':
				sec._access |= sec.ACCESS_W
			elif f == 'ALLOC':
				sec._access |= sec.ACCESS_R
				sec._flags.append(sec.ALLOC)
			elif f == 'EXECINSTR':
				type = sec.PROGCODE
				sec._access |= sec.ACCESS_X
				sec._arch = self._arch
			# TODO: determine if any of these are useful
			#elif f == 'MERGE':
			#elif f == 'STRINGS':
			#elif f == 'INFO_LINK':
			#elif f == 'LINK_ORDER':
			#elif f == 'OS_NONCONFORMING':
			#elif f == 'GROUP':
			#elif f == 'TLS':
		
		sec._type = type

	def __section_phdr_details(self, sec, phdr):
		sec_type = { 'Null' : sec.FILEHDR, 
				'Load' : sec.PROGDATA, 
				'Dynamic' : sec.FILEHDR, 
				'Interp' : sec.FILEHDR, 
				'Note' : sec.NOTE, 
				'Shlib' : sec.IMPORT,
				'Phdr' : sec.FILEHDR, 
				'TLS' : sec.FILEHDR }
		try:
			type = sec_type[phdr.type]
		except KeyError, e:
			type = sec.FILEHDR
		
		if phdr.type == 'Load':
			sec._flags.append(sec.ALLOC)
		
		for f in phdr.flags.split('|'):
			if f == 'R':
				sec._access |= sec.ACCESS_R
			elif f == 'W':
				sec._access |= sec.ACCESS_W
			elif f == 'X':
				type = sec.PROGCODE
				sec._access |= sec.ACCESS_X
				sec._arch = self._arch
		
		sec._type = type

	def __create_sections_from_shdr(self):
		sections = []
		
		self.__section_list.sort(lambda a,b: cmp(a.offset, b.offset))
		# create BGO sections based on ELF sections
		for sh in self.__section_list:
			if sh.flags.find('ALLOC') == -1: 
				# ignore sections that are not allocated
				continue
			# create new section
			s = section.Section(self, sh.name, sh.offset, 
					sh.size, sh.addr, self.__endian, 
					self.__word_size)
			# add section details
			self.__section_shdr_details(s, sh)
			# save in set File._sections
			self._sections.add( s )
			# add to local list 
			sections.append(s)
		
		sections.sort(lambda a, b: cmp(a.offset(), b.offset()))
		self.__segment_list.sort(lambda a,b: cmp(a.offset, b.offset))
		
		# create additional sections for unhandled, allocated
		# program segments.
		num = 1
		for ph in self.__segment_list:
			if ph.type != 'Load':
				# only interested in allocated segments
				continue
			
			# make a list of all sections in this segment
			sec = []
			for s in sections:
				if s.offset() >= ph.offset and \
					s.offset() < (ph.offset + ph.mem_size):
					sec.append(s)
			
			# if there are not any sections...
			if len(sec) < 1:
				# create section for entire segment
				new_s = section.Section( self, 
					'elf_' + str(num), ph.offset, 
					ph.mem_size, ph.vaddr,
					self.__endian, self.__word_size)
				self.__section_phdr_details(new_s, ph)
				self._sections.add(new_s)
				
				num += 1
				continue
			
			s = sec[0]
			if ph.offset < s.offset():
				# new section at start of segment
				if s.offset() < (ph.offset + ph.mem_size):
					size = s.offset() - ph.offset
				else :
					size = ph.mem_size
				
				new_s = section.Section( self, 
					'elf_' + str(num), ph.offset, 
					size, ph.vaddr, self.__endian, 
					self.__word_size)
				self.__section_phdr_details(new_s, ph)
				self._sections.add(new_s)
				
				num += 1
			
			last = sec[0]
			for s in sec[1:]:
				# if there is a gap between two segments
				diff = s.offset() - (last.offset()+last.size())
				if diff > 0:
					# create a section
					new_s = section.Section( self,
						'elf_' + str(num), 
						last.offset() + last.size(), 
						diff, 
						last.load_addr() + \
						last.size(),
						self.__endian, self.__word_size)
					self.__section_phdr_details(new_s, ph)
					self._sections.add(new_s)
					
					num += 1
					
				last = s
			
			# if there is unclaimed space at the end of the segment
			diff = (ph.offset + ph.mem_size) - \
			       (last.offset() + last.size())
			if diff > 0:
				# create a section
				new_s = section.Section( self, 
					'elf_' + str(num), 
						last.offset() + last.size(),
						diff, 
						last.load_addr() + \
						last.size(),
						self.__endian, self.__word_size)
				self.__section_phdr_details(new_s, ph)
				self._sections.add(new_s)
				num += 1


	def __create_sections(self):
		
		# check if there is a section header for code seg
		seg = self.__get_exec_segment()
		if seg == None:
			raise AssertionError, 'No executable program segment'
		
		for sh in self.__section_list:
			if sh.type == 'PROGBITS' and \
				sh.flags == 'ALLOC|EXECINSTR' and \
				sh.offset >= seg.offset and \
				(sh.offset + sh.size) <= \
				(seg.offset + seg.file_size):
				# elf section headers are sane: use them
				# to create the BGO sections
				self.__create_sections_from_shdr()
				return
		# create BGO sections from program headers
		num = 1
		for ph in self.__segment_list:
			if ph.type == 'Load':
				s = section.Section( self, 'elf_' + str(num), 
					ph.offset, ph.mem_size, ph.vaddr,
					self.__endian, self.__word_size)
				self.__section_phdr_details(s, ph)
				self._sections.add(s)
				num += 1
			elif ph.type == 'Dynamic':
				# metadata -- handle specific dynamic types
				continue
			else:
				continue

	def __section_headers(self):
		
		self.__section_list = []
		for i in range( 0, self.elf_header.shnum):
			offset = self.elf_header.shoff + \
			         (i * self.elf_header.shentsize)
			if offset > self._size:
				#raise AssertionError, 
				sys.stderr.write(
					"Section headers defined beyond EOF\n")
				break
			
			if self.elf_ident.file_class == '32' :
				sec = ElfSection32(self, offset)
			elif self.elf_ident.file_class == '64' :
				sec = ElfSection64(self, offset)
			else:
				# default to 32-bit
				sec = ElfSection(self, offset)
			
			self.__section_list.append(sec)
			
		# generate section names
		try:
			str_hdr = self.__section_list[self.elf_header.shstrndx]
		except IndexError, e:
			#raise AssertionError,"Section strtab defined beyond EOF"
			sys.stderr.write( "Section strtab defined beyond EOF\n")
			return
		
		strtab = self.read(str_hdr.offset, str_hdr.size) 
		for s in self.__section_list:
			try:
				names = strtab[s.name_raw:].split("\000")
				s.name =  names[0]
			except IndexError, e:
				sys.stderr.write('String extends beyond strtab')


	def __program_headers(self):
		self.__segment_list = []
		for i in range( 0, self.elf_header.phnum):
			offset = self.elf_header.phoff + \
			         (i * self.elf_header.phentsize)
			
			if self.elf_ident.file_class == '32' :
				sec = ElfSegment32(self, offset)
			elif self.elf_ident.file_class == '64' :
				sec = ElfSegment64(self, offset)
			else:
				# default to 32-bit
				sec = ElfSegment(self, offset)
			
			self.__segment_list.append(sec)

	def __str__(self):
		# MAGIC ident info
		buf = file.File.__str__(self) + "\n"
		# ELF header info
		buf += str(self.elf_ident) + "\n" + str(self.elf_header) + "\n"
		
		# program headers
		if len(self.__segment_list) > 0:
			buf += "\nProgram Segments:\n"
		for i in self.__segment_list:
			buf  += str(i) + "\n"
		
		# section headers
		if len(self.__section_list) > 0:
			buf += "\nSections:\n"
		for i in self.__section_list:
			buf  += str(i) + "\n"
		
		return buf


# -----------------------------------------------------------------------------
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = ELFFile( sys.argv[1], 'ELF 32' )
	print str(f)

	# Test code for BGO Sections
	sec = []
	for s in f.sections():
		sec.append(s)
	sec.sort(lambda a, b: cmp(a.offset(), b.offset()))
	print "\nBGO SECTIONS:\n"
	for s in sec:
		print str(s)
