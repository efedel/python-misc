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
# --elf--
from file_modules.ELF_Classes.EIdent import *
from file_modules.ELF_Classes.EHdr import *
from file_modules.ELF_Classes.ESHdr import *
from file_modules.ELF_Classes.ESym import *
from file_modules.ELF_Classes.ERel import *
from file_modules.ELF_Classes.EPHdr import *
from file_modules.ELF_Classes.EDyn import *

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
