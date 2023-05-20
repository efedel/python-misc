#!/usr/bin/python
'''
	Big O X86 Disassembler module

	This interfaces to the libdisasm module provided by libdisasm.

	Note that libdisasm expects the input bytes to be in a ByteArray
	class, which it defines via the SWIG %array_class directive. For
	this reason, disasm_address copies enough bytes to disassemble
	the largest x86 instruction into a ByteArray, and uses that for
	disassembly.
'''

if __name__ == "__main__":
	# fix for running from top-level dir
	import sys
	sys.path.append(".")

import math
import x86disasm as libdisasm	# libdisasm python module
# --bgo-- 
import BGModule
import bgdb
import BGDisasm as disasm	# big o disassembler class
import utils.set as set
# ============================================================================
# These entail a fairly extensive bit of code and have been broken out
# --x86--
from disasm_modules.x86_Classes.x86Enum import *
#from disasm_modules.x86_Classes.x86Insn import *
from disasm_modules.x86_Classes.x86OperandFactory import *
from disasm_modules.x86_Classes.x86InsnFactory import *

# ============================================================================
# globals!	don't freak out, they're just for module use.
MODULE_VERSION 	= 0.1
MODULE_NAME	= 'x86'
MODULE_AUTHOR	= 'mammon_'
MODULE_LICENSE	= 'LGPL'

# singleton instance of X86Disasm for use in stuff like reg_from_id()
libdis = None

# singleton instance of x86Module for getting DB IDs
x86_module = None


# ============================================================================
class x86Module(BGModule.Module):
	'''
	   BGO Module for disassembling x86 (IA32) object code
	'''
	'''
	# x86-specific CPU types
	CPU_8086 = "8086"
	CPU_80286 = "80286"
	CPU_80386 = "80386"
	CPU_80387 = "80387"
	CPU_80486 = "80486"
	CPU_PENTIUM = "Pentium"
	CPU_PENTIUMPRO = "Pentium Pro"
	CPU_PENTIUM2 = "Pentium 2"
	CPU_PENTIUM3 = "Pentium 3"
	CPU_PENTIUM4 = "Pentium 4"
	CPU_K6 = "K6"
	CPU_K7 = "K7"
	CPU_ATHLON = "Athlon"
	# x86-specific ISA type
	ISA_FPUMGT = "FPU/SIMD Management"
	ISA_MMX = "MMX"
	ISA_SSE1 = "SSE"
	ISA_SSE2 = "SSE 2"
	ISA_SSE3 = "SSE 3"
	ISA_3DNOW = "3D Now"
	# x86-specific insn types
	TYPE_PUSHREGS = "pushregs"
	TYPE_POPREGS = "popregs"
	TYPE_PUSHFLAGS = "pushflags"
	TYPE_POPFLAGS = "popflags"
	TYPE_STRCMP = "strcmp"
	TYPE_STRLOAD = "load str"
	TYPE_STRMOV = "move str"
	TYPE_STRSTORE = "store str"
	TYPE_TRANSLATE = "xlat"
	TYPE_ROL = "rol"
	TYPE_ROR = "ror"
	TYPE_FLAGSET = "fset"
	TYPE_FLAGCLEAR = "fclear"
	TYPE_FLAGTOG = "ftog"
	TYPE_LDPI = "ldpi fp"
	TYPE_LDZ = "ldz fp"
	TYPE_BCDCONV = "conv bcd"
	TYPE_SZCONV = "conv size"
	# names of constants
	CONST_PI = "pi"
	CONST_ZERO = "zero"
	# names of eflags
	EFLAG_CARRY = "cf"
	EFLAG_ZERO = "zf"
	EFLAG_OFLOW = "of"
	EFLAG_DIR = "df"
	EFLAG_SIGN = "sf"
	EFLAG_PARITY = "pf"
	EFLAG_AUX = "af"
	EFLAG_TRAP = "tf"
	EFLAG_INT = "if"
	# names of segment registers
	SEGREG_ES = "es"
	SEGREG_CS = "cs"
	SEGREG_SS = "ss"
	SEGREG_DS = "ds"
	SEGREG_FS = "fs"
	SEGREG_GS = "gs"
	'''

	def __init__(self):
		
		BGModule.Module.__init__(self, MODULE_NAME, MODULE_VERSION,
					       MODULE_AUTHOR, MODULE_LICENSE )
	
	# names instruction classes [needed for restore]
	_classnames = {	TYPE_PUSHREGS: 'PushRegs', TYPE_POPREGS: 'PopRegs',
			TYPE_PUSHFLAGS: 'PushFlags', TYPE_POPFLAGS: 'PopFlags',
			TYPE_STRCMP: 'StrCmp', TYPE_STRLOAD: 'StrLoad',
			TYPE_STRMOV: 'StrMove', TYPE_STRSTORE: 'StrStore',
			TYPE_TRANSLATE: 'Xlat', TYPE_ROL: 'RotateLeft',
			TYPE_ROR: 'RotateRight', TYPE_FLAGSET: 'SetFlag',
			TYPE_FLAGCLEAR: 'ClearFlag', TYPE_FLAGTOG: 'ToggleFlag',
			TYPE_LDPI: 'LoadPi', TYPE_LDZ: 'LoadZero',
			TYPE_BCDCONV: 'BcdConv', TYPE_SZCONV: 'SizeConv' }

	# db ids of instruction classes [needed for restore]
	_classes = {	TYPE_PUSHREGS:0, TYPE_POPREGS:0, TYPE_PUSHFLAGS:0,
			TYPE_POPFLAGS:0, TYPE_STRCMP:0, TYPE_STRLOAD:0,
			TYPE_STRMOV:0, TYPE_STRSTORE:0, TYPE_TRANSLATE:0,
			TYPE_ROL:0, TYPE_ROR:0, TYPE_FLAGSET:0,
			TYPE_FLAGCLEAR:0, TYPE_FLAGTOG:0, TYPE_LDPI:0,
			TYPE_LDZ:0, TYPE_BCDCONV:0, TYPE_SZCONV:0 }

	# db ids of cpu types
	_cpus = { 	CPU_8086:0, CPU_80286:0, CPU_80386:0, CPU_80387:0,
			CPU_80486:0, CPU_PENTIUM:0, CPU_PENTIUMPRO:0,
			CPU_PENTIUM2:0, CPU_PENTIUM3:0, CPU_PENTIUM4:0,
			CPU_K6:0, CPU_K7:0, CPU_ATHLON:0 }

	# db ids of isa types
	_isas = {	ISA_FPUMGT:0, ISA_MMX:0, ISA_SSE1:0, ISA_SSE2:0,
			ISA_SSE3:0, ISA_3DNOW:0 }

	# db ids of instruction minor types
	_types = {	TYPE_PUSHREGS:0, TYPE_POPREGS:0, TYPE_PUSHFLAGS:0,
			TYPE_POPFLAGS:0, TYPE_STRCMP:0, TYPE_STRLOAD:0,
			TYPE_STRMOV:0, TYPE_STRSTORE:0, TYPE_TRANSLATE:0,
			TYPE_ROL:0, TYPE_ROR:0, TYPE_FLAGSET:0,
			TYPE_FLAGCLEAR:0, TYPE_FLAGTOG:0, TYPE_LDPI:0,
			TYPE_LDZ:0, TYPE_BCDCONV:0, TYPE_SZCONV:0 }

	# db ids of eflags bit operands
	_bitops = {	EFLAG_CARRY:0, EFLAG_ZERO:0, EFLAG_OFLOW:0,
			EFLAG_DIR:0, EFLAG_SIGN:0, EFLAG_PARITY:0,
			EFLAG_AUX:0, EFLAG_TRAP:0, EFLAG_INT:0}

	_eflag_name = {	EFLAG_CARRY:'Carry', EFLAG_ZERO:'Zero', 
			EFLAG_OFLOW:'Overflow', EFLAG_DIR:'Direction', 
			EFLAG_SIGN:'Sign', EFLAG_PARITY:'Parity',
			EFLAG_AUX:'Auxiliary', EFLAG_TRAP:'Trap',
			EFLAG_INT:'Interrupt Enable'}

	_eflag_pos = {	EFLAG_CARRY:0, EFLAG_ZERO:6, EFLAG_OFLOW:11,
			EFLAG_DIR:10, EFLAG_SIGN:7, EFLAG_PARITY:2,
			EFLAG_AUX:4, EFLAG_TRAP:8, EFLAG_INT:9}

	# db ids of constants
	_consts = { 	CONST_PI : 0, CONST_ZERO: 0 }

	# values of constants
	_constvals = {	CONST_PI : math.pi, CONST_ZERO: 0 }

	_eflags_id = None

	def new_install(self):
		'''
		   insert types, etc into db
		'''
		# get db id for each instruction class name
		for c in self._classes.iterkeys():
			self._classes[c] = self._class_insert(c)

		# get db id for each cpu type
		for c in self._cpus.iterkeys():
			self._cpus[c] = self._cpu_insert(c)

		# get db id for each isa type
		for c in self._isas.iterkeys():
			self._isas[c] = self._isa_insert(c)

		# get db id for each instruction type
		for c in self._types.iterkeys():
			self._types[c] = self._type_insert(c)

		# get db id for each eflags bit operand
		self._eflags_insert()
		for c in self._bitops.iterkeys():
			self._bitops[c] = self._bitop_insert(c)

		# get db id for each constant
		for c in self._consts.iterkeys():
			self._consts[c] = self._const_insert(c)


	def upgrade_install(self, version):
		'''
		   get db ids for types, etc
		'''
		# get db id for each instruction class name
		for c in self._classes.iterkeys():
			id = self._class_select(c)
			if id is not None:
				self._classes[c] = id
			else:
				self._classes[c] = self._class_insert(c)

		# get db id for each cpu type
		for c in self._cpus.iterkeys():
			id = self._cpu_select(c)
			if id is not None:
				self._cpus[c] = id
			else:
				self._cpus[c] = self._cpu_insert(c)

		# get db id for each isa type
		for c in self._isas.iterkeys():
			id = self._isa_select(c)
			if id is not None:
				self._isas[c] = id
			else:
				self._isas[c] = self._isa_insert(c)

		# get db id for each instruction type
		for c in self._types.iterkeys():
			id = self._type_select(c)
			if id is not None:
				self._types[c] = id
			else:
				self._types[c] = self._type_insert(c)

		# get db id for each eflags bit operand
		self._eflags_id = self._eflags_select()
		if self._eflags_id is None:
			self._eflags_insert()

		for c in self._bitops.iterkeys():
			id = self._bitop_select(c)
			if id is not None:
				self._bitops[c] = id
			else:
				self._bitops[c] = self._bitop_insert(c)

		# get db id for each constant
		for c in self._consts.iterkeys():
			id = self._const_select(c)
			if id is not None:
				self._consts[c] = id
			else:
				self._consts[c] = self._const_insert(c)


	# Methods to insert rows into the DB
	def _class_insert(self, name):
		return self.db().insert( 'module_class', 
			{ 'classname' : name, 
			  'filename' : 'disasm_modules.x86',
			  'module' : self.db_id() } )

	def _cpu_insert(self, name):
		return self.db().insert( 'insn_cpu', { 'name' : name } )

	def _isa_insert(self, name):
		return self.db().insert( 'insn_isa', { 'name' : name } )

	def _type_insert(self, name):
		return self.db().insert( 'insn_minor_type', { 'name' : name } )

	def _eflags_insert(self):
		reg = libdis.reg_from_id(libdis.flag_reg())
		eflags = cpureg_factory(reg, None)
		# create op_reg row for %eflags
		reg_id = self.db().insert( 'op_reg', 
			{ 'reg_id' : eflags.id(),
			  'mnemonic': eflags.mnemonic(),
			  'type' : eflags.type_str(),
			  'size' : eflags.size() } )
		# create operand def for %eflags row
		self._eflags_id = self.db().insert( 'op_def',
			{ 'type' : operand.Operand.TYPE_REG[1],
			  'value' : reg_id } )

	def _bitop_insert(self, name):
		id = self.db().insert( 'op_bit', 
			{ 'name' : self._eflag_name[name],
			  'mnemonic' : name,
			  'reg' : self._eflags_id,
			  'position' : self._eflag_pos[name] } )
		return self.db().insert( 'op_def', 
				{ 'type' : operand.Operand.TYPE_BIT[1], 
				  'value' : id } )
		


	def _const_insert(self, name):
		pass

	# Methods to retrieve rows from the DB
	def _class_select(self, name):
		return self.db().fetch_id( 'module_class', 
			{ 'classname' : name, 
			  'filename' : 'disasm_modules.x86',
			  'module' : self.db_id() } )

	def _cpu_select(self, name):
		return self.db().fetch_id( 'insn_cpu', { 'name' : name } )

	def _isa_select(self, name):
		return self.db().fetch_id( 'insn_isa', { 'name' : name } )

	def _type_select(self, name):
		return self.db().fetch_id( 'insn_minor_type', 
			{ 'name' : name } )

	def _eflags_select(self):
		reg_id = self.db().fetch_id( 'op_reg', 
			{ 'reg_id' : libdis.flag_reg() } )

		if reg_id is None:
			return None

		return self.db().fetch_id( 'op_def', 
			{  'type' : operand.Operand.TYPE_REG[1],
			   'value' : reg_id } )

	def _bitop_select(self, name):
		pass

	def _const_select(self, name):
		pass

	# Methods to return a tuple for different type fields
	def cpu(self, type):
		return (type, self._cpus[type])

	def isa(self, type):
		return (type, self._isas[type])

	def type(self, typename):
		return (typename, self._types[typename])


# ============================================================================

class x86Disasm(disasm.Disasm):
	bg_module = None	# instance of x86Module()

	def __init__(self, options=0):
		global libdis
		global x86_module

		# default-options libdisasm for register lookups
		if libdis is None:
			libdis = libdisasm.X86_Disasm()

		if self.bg_module is None:
			# singleton instance of bg module
			# for doing DB init
			x86Disasm.bg_module = x86Module()
		if x86_module is None:
			x86_module = x86Disasm.bg_module

		disasm.Disasm.__init__(self, options)

		self.__options = options
		self.__name = "x86"
		
		try:
			self.__disasm = libdisasm.X86_Disasm(options)

		except NotImplementedError, e:
			self.__disasm = libdisasm.X86_Disasm()
			#raise e
			# the normal import can fail when called from factory
			# no idea -- swig weirdness. this works though.
			#self.__disasm = libdisasm.X86_DisasmPtr(options)
			# was:
			#	d_class = getattr(libdisasm, "X86_DisasmPtr")
			#	self.__disasm = d_class(options)
		except Exception, e:
			raise e

		
	def disasm_address( self, disasm_buf, offset=0 ):
		''' disassemble a single x86 instruction '''
		
		# Expects an array('B')
		bytes = disasm_buf.bytes()
		if bytes.typecode != 'B':
			raise AssertionError, "Input is not unsigned char array"
			return
		
		buf_len = len( bytes )
		
		if offset > buf_len:
			raise AssertionError, "Offset exceeds array length"
			return
		
		rva = disasm_buf.offset_to_rva(offset)
		
		# make a C-style buffer of bytes
		size = self.__disasm.max_insn_size()
		if size > buf_len - offset:
			size = buf_len - offset
		data = libdisasm.byteArray( size )
		for i in range( size ):
			data[i] = bytes[offset + i]
		
		# disassemble insn-sized buffer, at offset 0
		insn = self.__disasm.disasm( data, size, rva, 0 )

		# disassemble the invariant bytes -- this will help
		# us cache instruction definitions later
		insn_inv = self.__disasm.disasm_invariant( data, size, rva, 0 )
		
		bg_insn = insn_factory( insn, disasm_buf )
		bg_insn._signature = insn_inv.bytes
		
		del insn	# just to be safe: it's from C
		del insn_inv
		
		return bg_insn



# =========================================================================



if __name__ == "__main__":
	d = libdisasm.X86_Disasm(0)
	print str(d)
	
	try:
		x = x86Disasm(0)
		print str(x)
	except Exception, e:
		print str(e)
