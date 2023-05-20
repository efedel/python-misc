#!/usr/bin/python
'''
	Big O AR File module
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
MODULE_NAME = 'AR'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


PE_FILE = 'ARFile'
PE_MOD_CLASS = 0

class ARIdent(object):
	# string 'ARMAG'
	_format = '8s'
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e
		
		try:
			hdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		self.magic = hdr[0]
		self.size = struct.calcsize(self._format)

class ARHeader(object):
	_format = '16s12s6s6s8s10s2s'
	def __init__(self, file, offset):
		size = struct.calcsize(self._format)
		try:
			buf = file.read( offset, size )
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		byte = struct.unpack('B', buf[0])
		if byte[0] == 0x0A:
			# hack to handle libc.a, which has an extra
			# \r before some filenames ... no idea why
			buf = file.read( offset + 1, size )
			size += 1
		
		try:
			hdr = struct.unpack(self._format, buf)
		except Exception, e:
			sys.stderr.write( str(e) )
			raise e

		self.name = hdr[0]
		self.date = hdr[1]
		self.uid = hdr[2]
		self.gid = hdr[3]
		self.mode = hdr[4]
		self.obj_size = hdr[5]
		self.fmag = hdr[6]

		self.size = size + int(self.obj_size)

		print 'POS: ' + hex(offset) + ' SIZE: ' + str(size) + \
		      ' FILE SIZE: ' + self.obj_size 
		# need to handle magic in path!
		# f = FileFactory.FileFactory()
	def __str__(self):
		buf = 'NAME ' + self.name + '\n'
		buf += 'DATE ' + self.date + '\n'
		buf += 'UID ' + self.uid + '\n'
		buf += 'GID ' + self.gid + '\n'
		buf += 'MODE ' + self.mode + '\n'
		buf += 'SIZE ' + self.obj_size + '\n'
		buf += 'FMAG ' + self.fmag + '\n'
		return buf
	
# -----------------------------------------------------------------------------
class ARFile(objfile.ObjFile):
	AR_FORMAT=('AR', 3)
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
		self._format = self.AR_FORMAT
		self.file_objects = []
		
		objfile.ObjFile.__init__(self, path, ident)
		

	def parse(self):
		pos = 0
		self.ident = ARIdent(self, 0)
		pos += self.ident.size
		while pos < self.size():
			file = ARHeader(self, pos)
			self.file_objects.append(file)
			pos += file.size
		

	def __str__(self):
		buf = 'Magic: ' + self.ident.magic + '\n'
		buf += 'File Objects:\n'
		for f in self.file_objects:
			buf += str(f) + '\n'
		
		return buf


# -----------------------------------------------------------------------------
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = ARFile( sys.argv[1], 'AR 32' )
	print str(f)
