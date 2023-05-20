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

import array			# for insn.bytes
import math			# for pi

import x86disasm as libdisasm	# libdisasm python module
# --bgo-- 
import BGModule
import bgdb
import BGInstruction as instr	# big o instruction class
import BGOperand as operand	# big o operand class
import BGDisasm as disasm	# big o disassembler class
import utils.set as set
# --bgo instruction types--
import BGInstructions.Arithmetic as Arith
import BGInstructions.Bit as Bit
import BGInstructions.Compare as Compare
import BGInstructions.ControlFlow as CFlow
import BGInstructions.LoadStore as LodStor
import BGInstructions.Logic as Logic
import BGInstructions.Misc as Misc
import BGInstructions.Stack as Stack
import BGInstructions.System as System
import BGInstructions.Trap as Trap

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


# ============================================================================
# instruction classes specific to x86 CPUs
class PushRegs(Stack.Instruction):
	__type = x86Module.TYPE_PUSHREGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PopRegs(Stack.Instruction):
	__type = x86Module.TYPE_POPREGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PushFlags(Stack.Instruction):
	__type = x86Module.TYPE_PUSHFLAGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PopFlags(Stack.Instruction):
	__type = x86Module.TYPE_POPFLAGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrCmp(Compare.Instruction):
	__type = x86Module.TYPE_STRCMP

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Compare.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrLoad(LodStor.Instruction):
	__type = x86Module.TYPE_STRLOAD

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrMove(LodStor.Instruction):
	__type = x86Module.TYPE_STRMOV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrStore(LodStor.Instruction):
	__type = x86Module.TYPE_STRSTORE

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class SetFlag(Bit.Instruction):
	__type = x86Module.TYPE_FLAGSET

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class ClearFlag(Bit.Instruction):
	__type = x86Module.TYPE_FLAGCLEAR

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class ToggleFlag(Bit.Instruction):
	__type = x86Module.TYPE_FLAGTOG

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class LoadPi(LodStor.Instruction):
	__type = x86Module.TYPE_LDPI

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class LoadZero(LodStor.Instruction):
	__type = x86Module.TYPE_LDZ

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class RotateLeft(Arith.Instruction):
	__type = x86Module.TYPE_ROL

	''' This will differ from ShiftLeft in its eval() '''
	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Arith.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class RotateRight(Arith.Instruction):
	__type = x86Module.TYPE_ROR

	''' This will differ from ShiftRight in its eval() '''
	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Arith.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class BcdConv(Misc.Instruction):
	__type = x86Module.TYPE_BCDCONV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class SizeConv(Misc.Instruction):
	__type = x86Module.TYPE_SZCONV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class Xlat(Misc.Instruction):
	__type = x86Module.TYPE_TRANSLATE

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

# ============================================================================
# Insn Conversion Routines
# boring and largely tasteless routines for converting libdisasm types to bgo
def convert_stackmod(insn):
	if insn.stack_mod != 0:
		return insn.stack_mod_val
	else:
		return None

#---------------------------------------------------------

def convert_cpu(insn):
	global x86_module
	cpu_map = {	libdisasm.cpu_8086: x86_module.cpu(x86Module.CPU_8086),
			libdisasm.cpu_80286: 
				x86_module.cpu(x86Module.CPU_80286),
			libdisasm.cpu_80386: 
				x86_module.cpu(x86Module.CPU_80386),
			libdisasm.cpu_80387: 
				x86_module.cpu(x86Module.CPU_80387),
			libdisasm.cpu_80486: 
				x86_module.cpu(x86Module.CPU_80486),
			libdisasm.cpu_pentium: 
				x86_module.cpu(x86Module.CPU_PENTIUM),
			libdisasm.cpu_pentiumpro: 
				x86_module.cpu(x86Module.CPU_PENTIUMPRO),
			libdisasm.cpu_pentium2: 
				x86_module.cpu(x86Module.CPU_PENTIUM2),
			libdisasm.cpu_pentium3: 
				x86_module.cpu(x86Module.CPU_PENTIUM3),
			libdisasm.cpu_pentium4: 
				x86_module.cpu(x86Module.CPU_PENTIUM4),
			libdisasm.cpu_k6: x86_module.cpu(x86Module.CPU_K6),
			libdisasm.cpu_k7: x86_module.cpu(x86Module.CPU_K7),
			libdisasm.cpu_athlon: 
				x86_module.cpu(x86Module.CPU_ATHLON) }

	return cpu_map.get(insn.cpu, instr.Instruction.CPU_UNKNOWN)

#---------------------------------------------------------

def convert_isa(insn):
	isa_map = {	libdisasm.isa_gp: instr.Instruction.ISA_GP,
			libdisasm.isa_fp: instr.Instruction.ISA_FP,
			libdisasm.isa_fpumgt: 
				x86_module.isa(x86Module.ISA_FPUMGT),
			libdisasm.isa_mmx: x86_module.isa(x86Module.ISA_MMX),
			libdisasm.isa_sse1: x86_module.isa(x86Module.ISA_SSE1),
			libdisasm.isa_sse2: x86_module.isa(x86Module.ISA_SSE2),
			libdisasm.isa_sse3: x86_module.isa(x86Module.ISA_SSE3),
			libdisasm.isa_3dnow: 
				x86_module.isa(x86Module.ISA_3DNOW),
			libdisasm.isa_sys: instr.Instruction.ISA_SYS }

	return isa_map.get(insn.isa, instr.Instruction.ISA_UNKNOWN)

#---------------------------------------------------------

def convert_prefixes(bginsn, insn):
	prefix_map = {	libdisasm.insn_rep_zero: 
				instr.Instruction.PREFIX_REP_ZERO,
			libdisasm.insn_rep_notzero: 
				instr.Instruction.PREFIX_REP_NOTZERO,
			libdisasm.insn_lock: 
				instr.Instruction.PREFIX_LOCK }

	bginsn._prefixes = []
	for p in prefix_map.iterkeys():
		if insn.prefix & p:
			bginsn._prefixes.append(prefix_map[p])

#---------------------------------------------------------

def convert_notes(bginsn, insn):
	note_map = {	libdisasm.insn_note_ring0: 
				instr.Instruction.NOTE_RING0,
			libdisasm.insn_note_smm: 
				instr.Instruction.NOTE_SMM,
			libdisasm.insn_note_serial: 
				instr.Instruction.NOTE_SERIAL }

	bginsn._flags = []
	for n in note_map.iterkeys():
		if insn.note & n:
			bginsn._flags.append(note_map[n])


#---------------------------------------------------------

def convert_flags_set(bginsn, insn):
	setflag_map = {libdisasm.insn_carry_set: 
				instr.Instruction.FLAGS_SET_CARRY,
			libdisasm.insn_zero_set: 
				instr.Instruction.FLAGS_SET_ZERO,
			libdisasm.insn_oflow_set: 
				instr.Instruction.FLAGS_SET_OFLOW,
			libdisasm.insn_dir_set: 
				instr.Instruction.FLAGS_SET_DIR,
			libdisasm.insn_sign_set: 
				instr.Instruction.FLAGS_SET_SIGN,
			libdisasm.insn_parity_set: 
				instr.Instruction.FLAGS_SET_PARITY,
			libdisasm.insn_carry_clear: 
				instr.Instruction.FLAGS_CLEAR_CARRY,
			libdisasm.insn_zero_clear: 
				instr.Instruction.FLAGS_CLEAR_ZERO,
			libdisasm.insn_oflow_clear: 
				instr.Instruction.FLAGS_CLEAR_OFLOW,
			libdisasm.insn_dir_clear: 
				instr.Instruction.FLAGS_CLEAR_DIR,
			libdisasm.insn_sign_clear: 
				instr.Instruction.FLAGS_CLEAR_SIGN,
			libdisasm.insn_parity_clear: 
				instr.Instruction.FLAGS_CLEAR_PARITY }
	bginsn._flags_set = []

	for f in setflag_map.iterkeys():
		if insn.flags_set & f:
			bginsn._flags_set.append(setflag_map[f])


#---------------------------------------------------------

def convert_flags_test(bginsn, insn):
	tstflag_map = {	libdisasm.insn_carry_set: 
				instr.Instruction.FLAGS_TEST_CARRY_SET,
			libdisasm.insn_zero_set: 
				instr.Instruction.FLAGS_TEST_ZERO_SET,
			libdisasm.insn_oflow_set: 
				instr.Instruction.FLAGS_TEST_OFLOW_SET,
			libdisasm.insn_dir_set: 
				instr.Instruction.FLAGS_TEST_DIR_SET,
			libdisasm.insn_sign_set: 
				instr.Instruction.FLAGS_TEST_SIGN_SET,
			libdisasm.insn_parity_set: 
				instr.Instruction.FLAGS_TEST_PARITY_SET,
			libdisasm.insn_carry_or_zero_set: 
				instr.Instruction.FLAGS_TEST_CARRY_OR_ZERO_SET,
			libdisasm.insn_zero_set_or_sign_ne_oflow: 
			instr.Instruction.FLAGS_TEST_ZERO_SET_OR_SIGN_NE_OFLOW }

	bginsn._flags_tested = []
	for f in tstflag_map.iterkeys():
		if insn.flags_tested & f:
			bginsn._flags_tested.append(tstflag_map[f])

# ============================================================================
# Operand conversion Routines
# more of the same...
def convert_op_type(op):
	op_type_map = {libdisasm.op_unused : operand.Operand.TYPE_UNUSED,
			libdisasm.op_register : operand.Operand.TYPE_REG,
			libdisasm.op_immediate : operand.Operand.TYPE_IMM,
			libdisasm.op_relative_near : 
				operand.Operand.TYPE_RELNEAR,
			libdisasm.op_relative_far : operand.Operand.TYPE_RELFAR,
			libdisasm.op_absolute : operand.Operand.TYPE_ABSOLUTE,
			libdisasm.op_expression : operand.Operand.TYPE_EXPR,
			libdisasm.op_offset : operand.Operand.TYPE_OFFSET }

	return op_type_map.get(op.type, operand.Operand.TYPE_UNK)


#---------------------------------------------------------
def convert_op_datatype(op):
	op_dtype_map = {libdisasm.op_byte: operand.Operand.DATATYPE_BYTE,
			libdisasm.op_word: operand.Operand.DATATYPE_HWORD,
			libdisasm.op_dword: operand.Operand.DATATYPE_WORD,
			libdisasm.op_qword: operand.Operand.DATATYPE_DWORD,
			libdisasm.op_dqword: operand.Operand.DATATYPE_QWORD,
			libdisasm.op_sreal: operand.Operand.DATATYPE_SREAL,
			libdisasm.op_dreal: operand.Operand.DATATYPE_DREAL,
			libdisasm.op_extreal: operand.Operand.DATATYPE_EXTREAL,
			libdisasm.op_bcd: operand.Operand.DATATYPE_BCD,
			libdisasm.op_ssimd: operand.Operand.DATATYPE_SSIMD,
			libdisasm.op_dsimd: operand.Operand.DATATYPE_DSIMD,
			libdisasm.op_sssimd: operand.Operand.DATATYPE_SSSIMD,
			libdisasm.op_sdsimd: operand.Operand.DATATYPE_SDSIMD,
			libdisasm.op_descr32: operand.Operand.DATATYPE_DESC32,
			libdisasm.op_descr16: operand.Operand.DATATYPE_DESC16,
			libdisasm.op_pdescr32: operand.Operand.DATATYPE_PDESC32,
			libdisasm.op_pdescr16: operand.Operand.DATATYPE_PDESC16,
			libdisasm.op_fpuenv: operand.Operand.DATATYPE_FPUENV,
			libdisasm.op_fpregset: operand.Operand.DATATYPE_FPUREGS
		}

	return op_dtype_map.get(op.datatype, operand.Operand.DATATYPE_UNKNOWN)


#---------------------------------------------------------
def convert_op_access(in_op, out_op):
	op_access_map = {libdisasm.op_read : operand.Operand.ACCESS_R,
			libdisasm.op_write : operand.Operand.ACCESS_W,
			libdisasm.op_execute : operand.Operand.ACCESS_X }

	out_op._access = 0
	for f in op_access_map.iterkeys():
		if in_op.access & f:
			out_op._access |= op_access_map[f]

#---------------------------------------------------------
def convert_op_flags(in_op, out_op):
	opflag_map = {	libdisasm.op_signed : operand.Operand.FLAGS_SIGN,
			libdisasm.op_string : operand.Operand.FLAGS_STR,
			libdisasm.op_constant : operand.Operand.FLAGS_CONST,
			libdisasm.op_pointer : operand.Operand.FLAGS_PTR,
			libdisasm.op_sysref : operand.Operand.FLAGS_SYSCALL,
			libdisasm.op_implied : operand.Operand.FLAGS_IMPLICIT,
			libdisasm.op_hardcode : operand.Operand.FLAGS_HARDCODE }
	segreg_map = { 	libdisasm.op_es_seg : x86Module.SEGREG_ES,
			libdisasm.op_cs_seg : x86Module.SEGREG_CS,
			libdisasm.op_ss_seg : x86Module.SEGREG_SS,
			libdisasm.op_ds_seg : x86Module.SEGREG_DS,
			libdisasm.op_fs_seg : x86Module.SEGREG_FS,
			libdisasm.op_gs_seg : x86Module.SEGREG_GS }

	out_op._flags = []

	for f in opflag_map.iterkeys():
		if in_op.flags & f:
			out_op._flags.append(opflag_map[f])

	for f in segreg_map.iterkeys():
		if in_op.flags & f:
			out_op._segreg = segreg_map[f]
			

# ============================================== Immediate Conversion
def convert_imm_val(op):
	if op.datatype == libdisasm.op_byte:
		if op.flags & libdisasm.op_signed:
			val = op.data.sbyte
		else:
			val = op.data.byte
	elif op.datatype == libdisasm.op_word:
		if op.flags & libdisasm.op_signed:
			val = op.data.sword
		else:
			val = op.data.word
	elif op.datatype == libdisasm.op_dword:
		if op.flags & libdisasm.op_signed:
			val = op.data.sdword
		else:
			val = op.data.dword
	elif op.datatype == libdisasm.op_qword:
		if op.flags & libdisasm.op_signed:
			val = op.data.sqword
		else:
			val = op.data.qword
	elif op.datatype == libdisasm.op_dqword:
		val = op.data.dqword
	else:
		val = op.data.offset
	return val

# ============================================== Register Conversion
def convert_reg_type(type):
	reg_type_map = {libdisasm.reg_gen: operand.Operand.REG_GENERAL,
			libdisasm.reg_in: operand.Operand.REG_IN,
			libdisasm.reg_out: operand.Operand.REG_OUT,
			libdisasm.reg_local: operand.Operand.REG_LOCAL,
			libdisasm.reg_fpu: operand.Operand.REG_FPU,
			libdisasm.reg_seg: operand.Operand.REG_SEG,
			libdisasm.reg_simd: operand.Operand.REG_SIMD,
			libdisasm.reg_sys: operand.Operand.REG_SYS,
			libdisasm.reg_sp: operand.Operand.REG_SP,
			libdisasm.reg_fp: operand.Operand.REG_FP,
			libdisasm.reg_pc: operand.Operand.REG_PC,
			libdisasm.reg_retaddr: operand.Operand.REG_RETADDR,
			libdisasm.reg_cond: operand.Operand.REG_CC,
			libdisasm.reg_zero: operand.Operand.REG_ZERO,
			libdisasm.reg_ret: operand.Operand.REG_RET,
			libdisasm.reg_src: operand.Operand.REG_STRSRC,
			libdisasm.reg_dest: operand.Operand.REG_STRDEST,
			libdisasm.reg_count: operand.Operand.REG_COUNTER }

	regtype = []

	for r in reg_type_map.iterkeys():
		if type & r:
			regtype.append(reg_type_map[r])
	if not len(regtype):
		regtype.append(operand.Operand.REG_UNKNOWN)
	return regtype

def cpureg_factory(x86_reg, get_alias):
	global libdis
	if x86_reg.id == 0:
		return None

	# if this is called from Expression, it will need an alias...
	if get_alias is not None and x86_reg.alias != 0:
		alias_reg = libdis.reg_from_id(x86_reg.alias)
		alias = cpureg_factory(alias_reg, None)
	else:
		alias = None

	type = convert_reg_type(x86_reg.type)

	reg = operand.op.CpuRegister(x86_reg.id, x86_reg.name, type, \
		x86_reg.size, alias, x86_reg.shift)

	return reg
	
def register_factory(bginsn, order, x86_reg):
	global libdis
	if x86_reg.id == 0:
		return None
		
	# get aliased register
	#FIXME: register aliasing seems broken
	if x86_reg.alias != 0:
		alias_reg = libdis.reg_from_id(x86_reg.alias)
		alias = cpureg_factory(alias_reg, None)
	else:
		alias = None

	# register type: array of strings
	type = convert_reg_type(x86_reg.type)

	reg = operand.Register(bginsn, order, x86_reg.id, x86_reg.name,\
				type, x86_reg.size, alias, x86_reg.shift)

	return reg

# ============================================== Expression Conversion
def expression_factory(bginsn, order, exp):
	#TODO: make sure this is correct! do we have to cast
	#      if < long or ! signed?
	disp = exp.disp
			
	base = cpureg_factory( exp.base, True)

	index = cpureg_factory( exp.index, True)

	op = operand.EffectiveAddress(bginsn, order, disp, base, \
		             index, exp.scale)
	return op

# ============================================== Operand Factory
def operand_factory(bginsn, order, x86_op):
	# TODO: name operand
	if x86_op.type == libdisasm.op_register:
		op = register_factory(bginsn, order, x86_op.data.reg)
		
	elif x86_op.type == libdisasm.op_immediate:
		val = convert_imm_val(x86_op)
		op = operand.Immediate(bginsn, order, val)
			
	elif x86_op.type == libdisasm.op_relative_near:
		op = operand.Relative(bginsn, order, 'near',
			x86_op.data.relative_near,
			bginsn._offset + x86_op.data.relative_near,
			bginsn._address + bginsn._size + 
			x86_op.data.relative_near
					  )
			
	elif x86_op.type == libdisasm.op_relative_far:
		op = operand.Relative(bginsn, order, 'far',
			x86_op.data.relative_far,
			bginsn._offset + x86_op.data.relative_far,
			bginsn._address + bginsn._size + 
			x86_op.data.relative_far
						 )
			
	elif x86_op.type == libdisasm.op_absolute:
		op = operand.Address(bginsn, order, x86_op.data.address)
			
	elif x86_op.type == libdisasm.op_expression:
		op = expression_factory(bginsn, order, \
			x86_op.data.expression )
			
	elif x86_op.type == libdisasm.op_offset:
		op = operand.Offset(bginsn, order, x86_op.data.offset)
			
	else:
		return None
		
	# operand type : string
	op._type = convert_op_type(x86_op)
		
	# operand datatype : string
	op._datatype = convert_op_datatype(x86_op)
		
	# ways in which insn accesses operand (rwx) : unsigned int
	convert_op_access(x86_op, op)
		
	# operand flags : array of strings
	convert_op_flags(x86_op, op)
		
	return op

def convert_operands(bginsn, insn):
	op_list = insn.operand_list()
	node = op_list.first()
	order = 0
	while node is not None:
		op = operand_factory(bginsn, order, node.op)
		if op is not None:
			bginsn._operands.add(op)
		node = op_list.next()
		order += 1


# ============================================================================
# Initialize Instruction Object 

def init_insn(bginsn, insn, disasm_buf):
	''' Perform initialization common to all x86 instructions '''
	bginsn._disasm = "x86"
		
	# offset of insn in buffer : unsigned int
	bginsn._offset = disasm_buf.rva_to_file_offset(insn.addr)
	bginsn._address = insn.addr

	# number of bytes in insn : unsigned int
	bginsn._size = insn.size

	# all bytes in insn : array of bytes
	if disasm_buf is not None:
		bytes = disasm_buf[bginsn._offset:bginsn._offset+bginsn._size]
		bginsn._bytes = array.array('B', bytes).tostring()
	else:
		bginsn._bytes = None

	# insn flags : array of strings
	convert_notes(bginsn, insn)
	# insn (all) prefixes : array of string
	convert_prefixes(bginsn, insn)
	# insn (mnemonic/printable) prefixes : string
	bginsn._prefix_mnemonic = insn.prefix_string
	# insn mnemonic : string
	bginsn._mnemonic = insn.mnemonic
		
	# insn 'group' or general type : string
	#bginsn._major_type = convert_group(insn)
	# insn 'type' or specific type : string
	#bginsn._minor_type = convert_type(insn)
		
	# CPU revision when insn was introduced : string
	bginsn._cpu = convert_cpu(insn)
	# ISA subset containing insn : string
	bginsn._isa = convert_isa(insn)
		
	# eflags set by insn : array of strings
	convert_flags_set(bginsn, insn)
	# eflags tested by insn : array of strings
	convert_flags_test(bginsn, insn)
		
	# modifications the insn makes to stack : signed int
	bginsn._stack_mod = convert_stackmod(insn)
		
	# not implemented in libdisasm yet
	# title of insn in opcode reference : string
	# bginsn._title = insn.title
	# description of insn in opcode reference : string
	# bginsn._description = insn.description
	# psuedocode for insn in opcode ref : string
	# bginsn._psuedocode = insn.psuedocode
		
	convert_operands(bginsn, insn)

def generic_factory(insn, disasm_buf, cls):
	bg_insn = cls(disasm_buf)
	init_insn(bg_insn, insn, disasm_buf)

	return bg_insn

def incdec_factory(insn, disasm_buf, cls):
	''' generates INC/DEC insns as ADD/SUB w/ an implicit operand 1 '''
	bg_insn = generic_factory(insn, disasm_buf, cls)

	# add implicit operand operand for value 1
	order = len(bg_insn._operands)
	op = operand.Immediate(bg_insn, order, 1);
	op._flags.append(op.FLAGS_IMPLICIT)
	op._flags.append(op.FLAGS_HARDCODE)
	op._datatype = op.DATATYPE_BYTE
	op._access = op.ACCESS_R

	bg_insn._operands.add(op)

	return bg_insn

def flag_factory(insn, disasm_buf, args):
	cls = args[0]
	val = args[1]

	bg_insn = generic_factory(insn, disasm_buf, cls)

	# add implicit operand for eflags
	order = len(bg_insn._operands)
	# get register for eflags
	eflags_reg = libdis.reg_from_id(libdis.flag_reg())
	op = register_factory(bg_insn, order, eflags_reg)
	op._flags.append(op.FLAGS_IMPLICIT)
	op._flags.append(op.FLAGS_HARDCODE)
	# TODO: FIXME
	op._access = op.ACCESS_R

	bg_insn._operands.add(op)

	# add implicit bit operand for flag
	order += 1
	# get op_bit for flag
	op = operand.Bit(bg_insn, order, 1);
	op._flags.append(op.FLAGS_IMPLICIT)
	op._flags.append(op.FLAGS_HARDCODE)
	op._datatype = op.DATATYPE_BYTE
	op._access = op.ACCESS_R
	op._op_def_id = x86Module._bitops[val]

	bg_insn._operands.add(op)

	return bg_insn

def load_factory(insn, disasm_buf, args):
	cls = args[0]
	name = args[1]
	bg_insn = generic_factory(insn, disasm_buf, cls)
	# get const from db
	# get value for const 
	# add implicit operand for value
	order = len(bg_insn._operands)
	op = operand.Immediate(bg_insn, order, 1);
	op._flags.append(op.FLAGS_IMPLICIT)
	op._flags.append(op.FLAGS_HARDCODE)
	op._datatype = op.DATATYPE_BYTE
	op._access = op.ACCESS_R

	bg_insn._operands.add(op)

	return bg_insn

# big nasty type mapping
# format :  LIBDISASM_TYPE : (factory_function, function_args)
#           function_args is usually the Class, but could be a tuple
# Most types are handled by generic_factory, but some need special handling
type_map = { 	
	libdisasm.insn_jmp : (generic_factory, CFlow.BranchAlways),
	libdisasm.insn_jcc : (generic_factory, CFlow.BranchCond), 
	libdisasm.insn_call : (generic_factory, CFlow.CallAlways),
	libdisasm.insn_callcc : (generic_factory, CFlow.CallCond), 
	libdisasm.insn_return : (generic_factory, CFlow.Return),
	libdisasm.insn_add : (generic_factory, Arith.Add ),
	libdisasm.insn_sub : (generic_factory, Arith.Sub),
	libdisasm.insn_mul : (generic_factory, Arith.Mul ),
	libdisasm.insn_div : (generic_factory, Arith.Div),
	libdisasm.insn_inc : (incdec_factory, Arith.Add ),
	libdisasm.insn_dec : (incdec_factory, Arith.Sub),
	libdisasm.insn_shl : (generic_factory, Arith.ShiftLeft ),
	libdisasm.insn_shr : (generic_factory, Arith.ShiftRight),
	libdisasm.insn_rol : (generic_factory, RotateLeft),
	libdisasm.insn_ror : (generic_factory, RotateRight),
	libdisasm.insn_and : (generic_factory, Logic.And),
	libdisasm.insn_or : (generic_factory, Logic.Or),
	libdisasm.insn_xor :(generic_factory, Logic.Xor ),
	libdisasm.insn_not :(generic_factory, Logic.Not),
	libdisasm.insn_neg :(generic_factory, Logic.Neg ),
	libdisasm.insn_push : (generic_factory, Stack.Push),
	libdisasm.insn_pop : (generic_factory, Stack.Pop),
	libdisasm.insn_pushregs : (generic_factory, PushRegs),
	libdisasm.insn_popregs : (generic_factory, PopRegs),
	libdisasm.insn_pushflags : (generic_factory, PushFlags),
	libdisasm.insn_popflags :  (generic_factory, PopFlags),
	libdisasm.insn_enter : (generic_factory, Stack.EnterFrame),
	libdisasm.insn_leave : (generic_factory, Stack.LeaveFrame),
	libdisasm.insn_test : (generic_factory, Compare.Test),
	libdisasm.insn_cmp : (generic_factory,  Compare.Compare),
	libdisasm.insn_mov : (generic_factory, LodStor.Move),
	libdisasm.insn_movcc : (generic_factory, LodStor.MoveCond), 
	libdisasm.insn_xchg : (generic_factory, LodStor.Exchange),
	libdisasm.insn_xchgcc :(generic_factory,  LodStor.ExchangeCond),
	libdisasm.insn_strcmp :(generic_factory, StrCmp),
	libdisasm.insn_strload : (generic_factory, StrLoad), 
	libdisasm.insn_strmov : (generic_factory, StrMove),
	libdisasm.insn_strstore : (generic_factory, StrStore),
	libdisasm.insn_translate : (generic_factory, Xlat),
	libdisasm.insn_bittest : (generic_factory, Compare.Test),
	libdisasm.insn_bitset : (generic_factory, Bit.Set),
	libdisasm.insn_bitclear : (generic_factory, Bit.Clear), 
	libdisasm.insn_clear_carry : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_CARRY)),
	libdisasm.insn_clear_zero : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_ZERO) ),
	libdisasm.insn_clear_oflow : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_OFLOW)),
	libdisasm.insn_clear_dir : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_DIR) ),
	libdisasm.insn_clear_sign : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_SIGN)),
	libdisasm.insn_clear_parity : 
		(flag_factory,(Bit.Clear, x86Module.EFLAG_PARITY)), 
	libdisasm.insn_set_carry : 
		(flag_factory,(Bit.Set, x86Module.EFLAG_CARRY)),
	libdisasm.insn_set_zero :
		(flag_factory,(Bit.Set, x86Module.EFLAG_ZERO) ),
	libdisasm.insn_set_oflow :
		(flag_factory,(Bit.Set, x86Module.EFLAG_OFLOW)),
	libdisasm.insn_set_dir : 
		(flag_factory,(Bit.Set, x86Module.EFLAG_DIR) ),
	libdisasm.insn_set_sign :
		(flag_factory,(Bit.Set, x86Module.EFLAG_SIGN)),
	libdisasm.insn_set_parity : 
		(flag_factory,(Bit.Set, x86Module.EFLAG_PARITY) ),
	libdisasm.insn_tog_carry : 
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_CARRY)),
	libdisasm.insn_tog_zero :
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_ZERO) ),
	libdisasm.insn_tog_oflow :
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_OFLOW)),
	libdisasm.insn_tog_dir : 
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_DIR) ),
	libdisasm.insn_tog_sign : 
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_SIGN)),
	libdisasm.insn_tog_parity : 
		(flag_factory,(Bit.Toggle, x86Module.EFLAG_PARITY)), 
	libdisasm.insn_fmov : (generic_factory, LodStor.Move),
	libdisasm.insn_fmovcc : (generic_factory, LodStor.MoveCond), 
	libdisasm.insn_fneg : (generic_factory, Logic.Neg),
	libdisasm.insn_fabs : (generic_factory, Arith.AbsoluteVal ),
	libdisasm.insn_fadd : (generic_factory, Arith.Add),
	libdisasm.insn_fsub : (generic_factory, Arith.Sub ),
	libdisasm.insn_fmul : (generic_factory, Arith.Mul),
	libdisasm.insn_fdiv : (generic_factory, Arith.Div ),
	libdisasm.insn_fsqrt : (generic_factory, Arith.SquareRoot),
	libdisasm.insn_fcmp : (generic_factory,  Compare.Compare),
	libdisasm.insn_fcos : (generic_factory, Arith.Cosine ),
	libdisasm.insn_fldpi : 
		(load_factory, (LodStor.Move, x86Module.CONST_PI)),
	libdisasm.insn_fldz : 
		(load_factory, (LodStor.Move, x86Module.CONST_ZERO)),
	libdisasm.insn_ftan : (generic_factory, Arith.Tangent), 
	libdisasm.insn_fsine : (generic_factory, Arith.Sine),
	libdisasm.insn_fsys : (generic_factory, System.SysCtl ),
	libdisasm.insn_int : (generic_factory, Trap.Trap),
	libdisasm.insn_intcc : (generic_factory, Trap.TrapCond ),
	libdisasm.insn_iret : (generic_factory, Trap.TrapReturn),
	libdisasm.insn_bound : (generic_factory, Trap.Bound ),
	libdisasm.insn_debug : (generic_factory, Trap.Debug),
	libdisasm.insn_trace : (generic_factory, Trap.Trace ),
	libdisasm.insn_invalid_op : (generic_factory, Trap.InvalidOpcode),
	libdisasm.insn_oflow : (generic_factory, Trap.Overflow ),
	libdisasm.insn_halt : (generic_factory, System.Halt),
	libdisasm.insn_in : (generic_factory, System.IOPortRead ),
	libdisasm.insn_out : (generic_factory, System.IOPortWrite),
	libdisasm.insn_cpuid : (generic_factory, System.CpuID), 
	libdisasm.insn_nop : (generic_factory, Misc.Nop),
	libdisasm.insn_bcdconv : (generic_factory, BcdConv),
	libdisasm.insn_szconv : (generic_factory, SizeConv)
}

def insn_factory(insn, disasm_buf):
	tpl = type_map.get(insn.type, (generic_factory, Misc.Unknown))

	fn = tpl[0]
	args = tpl[1]

	# disable autosave, just in case
	bg_insn = fn(insn, disasm_buf, args)
	# renable autosave, just in case

	return bg_insn


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
