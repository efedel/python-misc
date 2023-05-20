#!/usr/bin/python
'''
	Big O OMF File module
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
MODULE_NAME = 'OMF'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


PE_FILE = 'OMFFile'
PE_MOD_CLASS = 0


OMF_REC_UNK1 =     0x00
OMF_REC_UNK2 =     0x01
OMF_REC_UNK3 =     0x0A
OMF_REC_UNK4 =     0x67
OMF_REC_THEADR =   0x80
OMF_REC_LHEADR =   0x82
OMF_REC_COMENT =   0x88
OMF_REC_MODEND =   0x8A
OMF_REC_MODEND32 = 0x8B
OMF_REC_EXTDEF =   0x8C
OMF_REC_PUBDEF =   0x90
OMF_REC_PUBDEF32 = 0x91
OMF_REC_LINNUM =   0x94
OMF_REC_LINNUM32 = 0x95
OMF_REC_LNAMES =   0x96
OMF_REC_SEGDEF =   0x98
OMF_REC_SEGDEF32 = 0x99
OMF_REC_GRPDEF =   0x9A
OMF_REC_FIXUPP =   0x9C
OMF_REC_FIXUPP32 = 0x9D
OMF_REC_LEDATA =   0xA0
OMF_REC_LEDATA32 = 0xA1
OMF_REC_LIDATA =   0xA2
OMF_REC_LIDATA32 = 0xA3
OMF_REC_COMDEF =   0xB0
OMF_REC_BAKPAT =   0xB2
OMF_REC_BAKPAT32 = 0xB3
OMF_REC_LEXTDEF =  0xB4
OMF_REC_LEXTDEF32 =0xB5
OMF_REC_LPUBDEF =  0xB6
OMF_REC_LPUBDEF32 =0xB7
OMF_REC_LCOMDEF =  0xB8
OMF_REC_CEXTDEF =  0xBC
OMF_REC_COMDAT =   0xC2
OMF_REC_COMDAT32 = 0xC3
OMF_REC_LINSYM =   0xC4
OMF_REC_LINSYM32 = 0xC5
OMF_REC_ALIAS =    0xC6
OMF_REC_NBKPAT =   0xC8
OMF_REC_NBKPAT32 = 0xC9
OMF_REC_LLNAMES =  0xCA
OMF_REC_VERNUM =   0xCC
OMF_REC_VENDEXT =  0xCE
OMF_REC_UNK5 =     0xE3
OMF_REC_ARCHIVE =  0xF0


omf_rec_types = {
	OMF_REC_UNK1:None,
	OMF_REC_UNK2:None,
	OMF_REC_UNK3:None,
	OMF_REC_UNK4:None,
	OMF_REC_UNK5:None,
	OMF_REC_THEADR:None,
	OMF_REC_LHEADR:None,
	OMF_REC_COMENT:None,
	OMF_REC_MODEND:None,
	OMF_REC_MODEND32:None,
	OMF_REC_EXTDEF:None,
	OMF_REC_PUBDEF:None,
	OMF_REC_PUBDEF32:None,
	OMF_REC_LINNUM:None,
	OMF_REC_LINNUM32:None,
	OMF_REC_LNAMES:None,
	OMF_REC_SEGDEF:None,
	OMF_REC_SEGDEF32:None,
	OMF_REC_GRPDEF:None,
	OMF_REC_FIXUPP:None,
	OMF_REC_FIXUPP32:None,
	OMF_REC_LEDATA:None,
	OMF_REC_LEDATA32:None,
	OMF_REC_LIDATA:None,
	OMF_REC_LIDATA32:None,
	OMF_REC_COMDEF:None,
	OMF_REC_BAKPAT:None,
	OMF_REC_BAKPAT32:None,
	OMF_REC_LEXTDEF:None,
	OMF_REC_LEXTDEF32:None,
	OMF_REC_LPUBDEF:None,
	OMF_REC_LPUBDEF32:None,
	OMF_REC_LCOMDEF:None,
	OMF_REC_CEXTDEF:None,
	OMF_REC_COMDAT:None,
	OMF_REC_COMDAT32:None,
	OMF_REC_LINSYM:None,
	OMF_REC_LINSYM32:None,
	OMF_REC_ALIAS:None,
	OMF_REC_NBKPAT:None,
	OMF_REC_NBKPAT32:None,
	OMF_REC_LLNAMES:None,
	OMF_REC_VERNUM:None,
	OMF_REC_VENDEXT:None,
	OMF_REC_ARCHIVE:None }

def OMFRecordFactory(file, offset):
	type = struct.unpack('B', file.read(offset, 1))


	
# -----------------------------------------------------------------------------
class OMFFile(objfile.ObjFile):
	OMF_FORMAT=('OMF', 3)
	'''
	bg_module = None
	
	endian_strings = ( section.Section.ENDIAN_BIG,
				section.Section.ENDIAN_LITTLE,
				section.Section.ENDIAN_BIG)

	# cpu_strings: name of disasm module for cpu
	# key must match Ehdr.machine_strings key
	# these tuples are from File.py and the DB
	cpu_strings = { 
		3:file.File.OMFCH_X86,	# IA-32
		62:file.File.OMFCH_X8664  # AMD 64
	}
	'''

	def __init__(self, path=None, ident=None, db_id=None):
		
		# set defaults, load and parse
		self._format = self.OMF_FORMAT
		self.file_objects = []
		self.omf_records = []
		
		objfile.ObjFile.__init__(self, path, ident)
		

	def parse(self):
		pos = 0
		while pos < self.size():
			rec = OMFRecordFactory(self)
			self.omf_records.append(rec)
			pos += rec.size
			

	def __str__(self):
		buf = 'Records:\n'
		for r in self.omf_records:
			buf += str(r) + '\n'

		buf += 'File Objects:\n'
		for f in self.file_objects:
			buf += str(f) + '\n'
		
		return buf


# -----------------------------------------------------------------------------
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = OMFFile( sys.argv[1], 'OMF 32' )
	print str(f)
