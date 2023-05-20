#!/usr/bin/python
'''
	Big O AOUT File module
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
MODULE_NAME = 'AOUT'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


AOUT_FILE = 'AOUTFile'
AOUT_MOD_CLASS = 0


mach_type = { 0:'Sun', 1:'68010', 2:'68020', 3:'SPARC', 100:'i386', 
              151:'MIPS', 152:'MIPS2' }
OMAGIC = 0407	# object file, 'impure' executable
NMAGIC = 0410	# 'pure' executable
ZMAGIC = 0413	# demand-paged executable
QMAGIC = 0314 	# demand-pages w/ header in test. first page unmmaped.
CMAGIC= 0421	# core
# HDROFF = (1024 - sizeof(struct exec))
# #define N_TXTOFF(x) \
#  (N_MAGIC(x) == ZMAGIC ? _N_HDROFF((x)) + sizeof (struct exec) :	\
#   (N_MAGIC(x) == QMAGIC ? 0 : sizeof (struct exec)))
#define N_DATOFF(x)	(N_TXTOFF(x) + (x).a_text)
#define N_TRELOFF(x)	(N_DATOFF(x) + (x).a_data)
#define N_DRELOFF(x)	(N_TRELOFF(x) + N_TRSIZE(x))
#define N_SYMOFF(x)	(N_DRELOFF(x) + N_DRSIZE(x))
#define N_STROFF(x)	(N_SYMOFF(x) + N_SYMSIZE(x))
#/* Address of text segment in memory after it is loaded.  */
#define N_TXTADDR(x)	(N_MAGIC(x) == QMAGIC ? 4096 : 0)
#/* Address of data segment in memory after it is loaded.  */
#define SEGMENT_SIZE	1024
#define N_DATADDR(x) \
#  (N_MAGIC(x)==OMAGIC? (_N_TXTENDADDR(x))				\
#   : (_N_SEGMENT_ROUND (_N_TXTENDADDR(x))))
#define N_BSSADDR(x) (N_DATADDR(x) + (x).a_data)

nlist_type = { 0:'Undefined', 2:'Absolute', 4:'Text', 6:'Data',
               8: 'BSS', 15:'Function', 1:'Externa;', 
	       036:'Type', 0340:'Stab', 0xa:'Indr',
	       0x14:'SetA', 0x16:'SetT', 0x18:'SetD',
	       0x1A:'SetB', 0x1C'SetV' }
# last are set element symbols


class AOUTExec(object):
	_format = '8L'
	def is_valid_magic(self):

	def get_endian(self, buf):
		val = pack('L', 0x12345678)
		(native,) = struct.unpack( '=L', val)
		(little,) = struct.unpack( '<L', val)

		if native == little:
			self._mach_endian = '<'
		else:
			self._mach_endian = '>'

	def ident(self, buf, endian):
		(self._magic,) = struct.unpack( endian + 'L', buf)
		if endian == self._mach_endian:
			self._endian = '='
		else:
			self._endian = endian
		
	def __init__(self, file, offset):
		# TODO: determine endiannes
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		# this should really be in a library somewhere :)
		self.get_endian()

		# try this as a little-endian file
		self.ident(buf[0:3], '<')

		# try this as a big-endian file
		if not self.is_valid_magic():
			self.ident(buf[0:3], '>')
		# crap
		if self.is_valid_magic():
			raise AssertionError, 'Invalid AOUT file'

		format = self._endian + self._format
			
		
		
		try:
			hdr = struct.unpack(format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )

		# 7 components: EXEC header, TEXT seg, DATA seg, 
		#               TEXT Reloc, DATA Reloc, SYMTAB, STRTAB
		# NOTE these are in order. 0 size = not present
		self._midmag = hdr[0]
		self._text = hdr[1]	# size of .text in bytes
		self._data = hdr[2]	# size of .data in bytes
		self._bss = hdr[3]	# size of .bss
		self._syms = hdr[4]	# size of .symtab
		self._entry = hdr[5]	# entry point
		self._tr_sz = hdr[6]	# size of text reloc
		self._dr_sz = hdr[7]	# size of data reloc
	
class Reloc(object):
	_format = 'iI'
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			rel = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )

		self._address = rel[0]
		self._bitfield = rel[1]
		self._symbol_num = self._bitfield & 0x00FFFFFF
		self._pcrel = self._bitfield & 0x01000000
		self._length = self._bitfield & 0x06000000
		self._extern = self._bitfield & 0x08000000
		self._baserel = self._bitfield & 0x10000000
		self._jmptable = self._bitfield & 0x20000000
		self._relative = self._bitfield & 0x40000000
		self._copy = self._bitfield & 0x80000000

class Symbol(object):
	# nlist struct
	_format = 'lBbhL'
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			sym = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )

		self._un = sym[0]
		self._type = sym[1]
		self._other = sym[2]
		self._desc = sym[3]
		self._value = sym[4]

# -----------------------------------------------------------------------------
class AOUTFile(objfile.ObjFile):
	AOUT_FORMAT=('AOUT', 3)
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
		self._format = self.AOUT_FORMAT
		
		objfile.ObjFile.__init__(self, path, ident)
		

	def parse(self):
		self.exec_hdr = AOUTExec(self, 0)
		
		# create BigO sections
		#self.__create_sections()

	def __str__(self):
		# MAGIC ident info
		buf = file.File.__str__(self) + "\n"
		buf += str(self.mz_hdr) + '\n'
		buf += str(self.pe_hdr) + '\n'
		# AOUT header info
		#buf += str(self.elf_ident) + "\n" + str(self.elf_header) + "\n"
		for s in self.pe_sections:
			buf += str(s) + '\n'
		
		return buf


# -----------------------------------------------------------------------------
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = AOUTFile( sys.argv[1], 'AOUT 32' )
	print str(f)

	# Test code for BGO Sections
	sec = []
	for s in f.sections():
		sec.append(s)
	sec.sort(lambda a, b: cmp(a.offset(), b.offset()))
	print "\nBGO SECTIONS:\n"
	for s in sec:
		print str(s)
