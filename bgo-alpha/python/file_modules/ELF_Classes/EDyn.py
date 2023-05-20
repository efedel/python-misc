#!/usr/bin/python
'''
	Big O ELF File module
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

class ElfDynamic(object):
	_format = 'lI'

class ElfDynamic32(ElfDynamic):
	_format = 'lI'

class ElfDynamic64(ElfDynamic):
	_format = 'qQ'

