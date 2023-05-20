#!/usr/bin/python
'''
	Big O PE File module
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
MODULE_NAME = 'PE'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


PE_FILE = 'PEFile'
PE_MOD_CLASS = 0

class MZHeader(object):
	# 30 short, 1 long
	_format = '2sHHHHHHHHHHHHHHHHHHHHHHHHHHHHHI'
	file_class_strings = ( 'none', '32', '64' )
	data_strings = ( 'None', 'LSB (little endian)', 'MSB (big endian)' )
	os_abi_strings = { 0:'SysV', 1:'HPUX', 2:'NetBSD', 3:'Linux',
	                   255:'Standalone' }
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			mz_hd = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		self.offset = offset
		self.size = size
		# 64 bytes
		# page = 512 bytes
		# para = 16 bytes
		self.magic = mz_hd[0]
		self.last_page_size = mz_hd[1]
		# size of file / 512...
		# size = ((num_pages -1)*512)+last_page_size
		self.num_pages = mz_hd[2]
		# number of reloc entries
		self.reloc = mz_hd[3]
		# size of header / 16
		self.header_size_para = mz_hd[4]
		# min # 16-byte pages req to execute
		self.min_extra_para = mz_hd[5]
		# max # 16-byte pages req to execute, usually ffff
		self.max_extra_para = mz_hd[6]
		self.stackseg = mz_hd[7]
		self.stackptr = mz_hd[8]
		self.checksum = mz_hd[9]
		self.programcounter = mz_hd[10]
		self.codeseg = mz_hd[11]
		self.reloc_tbl_offset = mz_hd[12]
		# 0 or overlay num
		self.overlay_num = mz_hd[13]
		self.resv = mz_hd[14]
		self.resv = mz_hd[15]
		self.resv = mz_hd[16]
		self.resv = mz_hd[17]
		self.oem_id = mz_hd[18]
		self.oem_info = mz_hd[19]
		self.resv = mz_hd[20]
		self.resv = mz_hd[21]
		self.resv = mz_hd[22]
		self.resv = mz_hd[23]
		self.resv = mz_hd[24]
		self.resv = mz_hd[25]
		self.resv = mz_hd[26]
		self.resv = mz_hd[27]
		self.resv = mz_hd[28]
		self.resv = mz_hd[29]
		self.pe_hdr_offset = mz_hd[30]

		self.size = self.header_size_para * 16
		# create a stub class here
		self.stub_start = self.size
		self.stub_end = self.pe_hdr_offset - 1
		
		#self.file_class_raw = mz_hd[1]
		#try:
		#	self.file_class = self.file_class_strings[mz_hd[1]]
		#except IndexError, e:
		#	self.file_class = 'Invalid file class: ' + str(mz_hd[1])
		
	def __str__(self):
		# TODO: XML
		return 'Magic: ' + self.magic + \
		       '\tHeader Size: ' + str(self.header_size_para * 16) + \
		       '\nNum Pages: ' + str(self.num_pages) + \
		       '\tLast Page: ' + str(self.last_page_size) + \
		       '\tFile Size: ' + \
		       str(((self.num_pages - 1)*512) + self.last_page_size) + \
		       '\nNum Reloc: ' + str(self.reloc) + \
		       '\tReloc Offset: ' + hex(self.reloc_tbl_offset) + \
		       '\nMin Alloc: ' + hex(self.min_extra_para * 16) + \
		       '\nChecksum: ' + hex(self.checksum) + \
		       '\tOverlay #: ' + str(self.overlay_num) + \
		       '\tMax Alloc: ' + hex(self.max_extra_para * 16) + \
		       '\nSS: ' + hex(self.stackseg) + \
		       '\tSP: ' + hex(self.stackptr) + \
		       '\nCS: ' + hex(self.codeseg) + \
		       '\tIP: ' + hex(self.programcounter) + \
		       '\nOEM ID: ' + hex(self.oem_id) + \
		       '\tOEM Info: ' + hex(self.oem_info) + \
		       '\nPE Header: ' + hex(self.pe_hdr_offset)

class FileHeader(object):
	_format = 'HHIIIHH'
	def __init__(self, file, offset):
		self.size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, self.size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			hdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		self.offset = offset
		self.machine = hdr[0]
		self.num_sec = hdr[1]
		self.timestamp = hdr[2]
		self.symtab = hdr[3]
		self.num_sym = hdr[4]
		self.opt_sz = hdr[5]
		self.char = hdr[6]

	def __str__(self):
		return 'Machine: ' + hex(self.machine) + \
		       '\tCharacteristics: ' + hex(self.char) + \
		       '\tTimestamp: ' + hex(self.timestamp) + \
		       '\nOpt Size: ' + str(self.opt_sz) + \
		       '\tNum Sections: ' + str(self.num_sec) + \
		       '\nSymbol Table: ' + hex(self.symtab) + \
		       '\tNum Symbols: ' + str(self.num_sym)

class DataDir(object):
	_format = 'II'
	def __init__(self, file, offset):
		self.size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, self.size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			dir = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		self.offset = offset
		self.dir_rva = dir[0]
		self.dir_size = dir[1]
	def __str__(self):
		return 'RVA: ' + hex(self.dir_rva) + \
		       '\tSize: ' + str(self.dir_size)

class OptionalHeader(object):
	_format = 'HBBIIIIIIIIIHHHHHHIIIIHHIIIIII'
	def __init__(self, file, offset):
		self.size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, self.size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			hdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		self.offset = offset
		self.magic = hdr[0]
		self.linker_major = hdr[1]
		self.linker_minor = hdr[2]
		self.code_sz = hdr[3]
		self.data_sz = hdr[4]
		self.bss_sz = hdr[5]
		self.entry = hdr[6]
		self.code_base = hdr[7]
		self.data_base = hdr[8]
		self.image_base = hdr[9]
		self.sec_align = hdr[10]
		self.file_align = hdr[11]
		self.os_major = hdr[12]
		self.os_minor = hdr[13]
		self.image_major = hdr[14]
		self.image_minor = hdr[15]
		self.subsys_major = hdr[16]
		self.subsys_minor = hdr[17]
		self.resv = hdr[18]
		self.image_sz = hdr[19]
		self.hdr_sz = hdr[20]
		self.checksum = hdr[21]
		self.subsys = hdr[22]
		self.dll_char = hdr[23]
		self.stack_reserve = hdr[24]
		self.stack_commit = hdr[25]
		self.heap_reserve = hdr[26]
		self.heap_commit = hdr[27]
		self.loader_flags = hdr[28]
		self.num_data_dir = hdr[29]
		self.data_dirs = []

		# get data directories
		for i in range( self.num_data_dir):
			d = DataDir( file, offset + self.size )
			self.size += d.size
			self.data_dirs.append(d)

	def __str__(self):
		buf = 'Magic: ' + hex(self.magic) + \
		      '\tChecksum: ' + hex(self.checksum) + \
		      '\tVersion: ' + str(self.image_major) + '.' + \
		      str(self.image_minor) + \
		      '\nOS: ' + str(self.os_major) + '.' + \
		      str(self.os_minor) + \
		      '\tLinker: ' + str(self.linker_major) + '.' + \
		      str(self.linker_minor) + \
		      '\tLoader Flags: ' + hex(self.loader_flags) + \
		      '\nSubsystem: ' + hex(self.subsys) + ' ' + \
		      str(self.subsys_major) + '.' + \
		      str(self.subsys_minor) + \
		      '\nImage Base: ' + hex(self.image_base) + \
		      '\tImage Size: ' + str(self.image_sz) + \
		      '\nBSS Size: ' + str(self.bss_sz) + \
		      '\tHeader Size: ' + str(self.hdr_sz) + \
		      '\nCode Base: ' + hex(self.code_base) + \
		      '\tCode Size: ' + str(self.code_sz) + \
		      '\nData Base: ' + hex(self.data_base) + \
		      '\tData Size: ' + str(self.data_sz) + \
		      '\nStack Reserve: ' + hex(self.stack_reserve) + \
		      '\tStack Commit: ' + hex(self.stack_commit) + \
		      '\nHeap Reserve: ' + hex(self.heap_reserve) + \
		      '\tHeap Commit: ' + hex(self.heap_commit) + \
		      '\nFile Align: ' + hex(self.file_align) + \
		      '\tSection Align: ' + hex(self.sec_align) + \
		      '\nEntry Point: ' + hex(self.entry) + \
		      '\tDLL Characteristic: ' + hex(self.dll_char) + \
		      '\tNumDataDirs: ' + hex(self.num_data_dir) + \
		      '\nData Directories\n'
		for d in self.data_dirs:
			buf = buf + str(d) + '\n'
		return buf

class PEHeader(object):
	def __init__(self, file, offset):
		# get signature
		sig_format = 'I'
		sig_size = struct.calcsize(sig_format)
		try:
			buf = file.read( offset, sig_size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			sig = struct.unpack(sig_format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		self.offset = offset
		self.sig = sig[0]
		# get file header
		self.file_hdr = FileHeader( file, offset + sig_size )
		# get optional header
		self.opt_hdr = OptionalHeader( file, offset + sig_size + \
			self.file_hdr.size )
		self.size = sig_size + self.file_hdr.size + self.opt_hdr.size

	def __str__(self):
		return 'Signature:' + hex(self.sig) + '\n' + \
		       str(self.file_hdr) + '\n' + \
		       str(self.opt_hdr) + '\n' 


class PESection(object):
	'''
	type_strings = { 0:'NULL', 1:'PROGBITS', 2:'SYMTAB', 3:'STRTAB', 
			 0x6fffffff:'GNU_VERSION_SYMTAB'};

	flag_strings = { 1:'WRITE', 2:'ALLOC', 4:'EXECINSTR', 8:'MERGE',
			128:'OS_NONCONFORMING', 256:'GROUP', 512:'TLS' }

	# default to 32-bit format
	'''
	_format = '8sIIIIIIHHI';

	def __init__(self, file, offset):
		self.size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, self.size )
			if len(buf) < self.size:
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
		
		self.name = shdr[0]
		self.virtual_size = shdr[1]
		self.rva = shdr[2]
		self.raw_data_sz = shdr[3]
		self.raw_data = shdr[4]
		self.reloc = shdr[5]
		self.line_num = shdr[6]
		self.num_reloc = shdr[7]
		self.num_line_num = shdr[8]
		self.char = shdr[9]

	def __str__(self):
		return  'Name: ' + self.name + \
			'\tCharacteristics: ' + hex(self.char) + \
			'\nVirtual Address: ' + hex(self.rva) + \
			'\tVirtual Size: ' + str(self.virtual_size) + \
			'\nRaw Data: ' + hex(self.raw_data) + \
			'\tRaw Data Size: ' + str(self.raw_data_sz) + \
			'\nRelocations: ' + hex(self.reloc) + \
			'\tNum Relocs: ' + str(self.num_reloc) + \
			'\nLine Numbers: ' + hex(self.line_num) + \
			'\tNum Line #: ' + str(self.num_line_num)
			

# -----------------------------------------------------------------------------
class PEFile(objfile.ObjFile):
	PE_FORMAT=('PE', 3)
	'''
	bg_module = None
	
	endian_strings = ( section.Section.ENDIAN_BIG,
				section.Section.ENDIAN_LITTLE,
				section.Section.ENDIAN_BIG)

	# cpu_strings: name of disasm module for cpu
	# key must match Ehdr.machine_strings key
	# these tuples are from File.py and the DB
	cpu_strings = { 
		3:file.File.ARCH_X86,	# IA-32
		62:file.File.ARCH_X8664  # AMD 64
	}
	'''

	def __init__(self, path=None, ident=None, db_id=None):
		
		# set defaults, load and parse
		self._format = self.PE_FORMAT
		
		objfile.ObjFile.__init__(self, path, ident)
		

	def parse(self):
		self.mz_hdr = MZHeader(self, 0)
		# handle PE ident
		#self.elf_ident = EIdent(self, 0)
		#self._type = self.TYPE_EXEC
		
		# handle PE header
		self.pe_hdr = PEHeader(self, self.mz_hdr.pe_hdr_offset)
		#if self.elf_ident.file_class == '32' :
		#	self.elf_header = Ehdr32(self, 0)
		#	self.__word_size = 4
		#elif self.elf_ident.file_class == '64' :
		#	self.elf_header = Ehdr64(self, 0)
		#	self.__word_size = 8
		#else:
			# for now we default to 32-bit, maybe change to error
			# later...
		#	sys.stderr.write('Warning: Unknown PE class ' + \
		#	                  self.elf_ident.file_class + "\n" )
		#	self.elf_header = Ehdr(self, 0)
		#	self.__word_size = 4
		
		# add elf entry point
		#self._entry.append(self.elf_header.entry)
		
		# NOTE: elf sections and segments are different from
		#       bgo sections. all the elf stuff is created first,
		#       and the bgo stuff is created based on that info.
		
		self.pe_sections = []
		sec_offset = self.pe_hdr.offset + self.pe_hdr.size
		for s in range(self.pe_hdr.file_hdr.num_sec):
			sec = PESection(self, sec_offset)
			self.pe_sections.append( sec )
			sec_offset += sec.size

		# handle section headers
		#self.__section_headers()
		
		# handle program segment headers
		#self.__program_headers()
		
		# handle sections
		# handle program segments
		
		# create BigO sections
		#self.__create_sections()

		data_dirs = ('Export Table', 'Import Table', 'Resource Table',
			     'Exception Table', 'Certificate Table', 
			     'Base Relocation Table', 'Debug', 'Architecture',
			     'Global Pointer', 'Thread Local Storage',
			     'Load Config Table', 'Bound Import Table',
			     'Import Address Table', 'Delay Import Descr',
			     'COM+ Runtime', 'Reserved')
		for i in range(0, len(data_dirs)):
			if self.pe_hdr.opt_hdr.num_data_dir >= i+1:
				d = self.pe_hdr.opt_hdr.data_dirs[i]
				print data_dirs[i] + ': ' + str(d.dir_size) + \
				      ' BYTES AT ' + str(d.dir_rva)
		# sample export handling
		# sample import handling
		# sample reloc handling
		# sample resource handling
		# sample debug handling

	def __str__(self):
		# MAGIC ident info
		buf = file.File.__str__(self) + "\n"
		buf += str(self.mz_hdr) + '\n'
		buf += str(self.pe_hdr) + '\n'
		# PE header info
		#buf += str(self.elf_ident) + "\n" + str(self.elf_header) + "\n"
		for s in self.pe_sections:
			buf += str(s) + '\n'
		
		return buf


# -----------------------------------------------------------------------------
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = PEFile( sys.argv[1], 'PE 32' )
	print str(f)

	# Test code for BGO Sections
	sec = []
	for s in f.sections():
		sec.append(s)
	sec.sort(lambda a, b: cmp(a.offset(), b.offset()))
	print "\nBGO SECTIONS:\n"
	for s in sec:
		print str(s)
