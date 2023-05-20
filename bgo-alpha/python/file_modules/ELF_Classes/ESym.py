#!/usr/bin/python
'''
	Big O ELF File module
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

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

