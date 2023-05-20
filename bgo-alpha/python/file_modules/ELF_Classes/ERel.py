#!/usr/bin/python
'''
	Big O ELF File module
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

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
