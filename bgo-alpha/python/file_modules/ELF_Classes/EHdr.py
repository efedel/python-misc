#!/usr/bin/python
'''
	Big O ELF File module: EHdr
'''

import sys
import struct
sys.path.append(".")
# -- bgo --

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

