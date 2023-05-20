#!/usr/bin/python
'''
	Big O Instruction Operand Class
'''

# --bgo--
import utils.set as set

#-------------------------------------------------------------------------
# Operand

class Operand(object):
	'''
	Operand is the base class for all Big O operands.
	Operand provides the following basic attributes:
	access := bitmask ACCESS_READ, ACCESS_WRITE, ACCESS_EXEC
	flags :=
	'''
	def __init__(self, insn, order, type=None):
		self._insn = insn
		self._datatype = self.DATATYPE_UNKNOWN
		self._access = 0
		self._flags = []
		self._order = order
		self._segreg = None
		self._name = 'op' + str(order)
		if type is None:
			type = self.TYPE_UNK
		self._type = type

	def __str__(self):
		buf = "<operand type='Unknown'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self._datatype) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"
		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"
		
		buf = buf + "</operand>\n"
		return buf
	
	def __repr__(self):
		return self.__str__()
	
	def __hash__(self):
		#return self._order	
		pass
	
	def __cmp__(self):
		pass
	
	def type(self):
		return self._type[0]

	def datatype(self):
		return self._datatype[0]

	def flags(self):
		return iter(self._flags)

	def flags_str(self):
		str = ''

		for f in self._flags:
			if str == '':
				str = f
			else:
				str = '|' + f

		return str

	def order(self):
		return self._order

	def name(self):
		return self._name

	def access(self):
		return self._access
	
	def size(self):
		''' size of operand datatype in bytes '''
		return self._datatype[2]

	def isimplicit(self):
		return self.FLAGS_IMPLICIT in self._flags

	def isexplicit(self):
		return self.FLAGS_IMPLICIT not in self._flags

	def istrap(self):
		'''
		   Is the operand used as an index into the interrupt
		   vector table?
		'''
		return self.FLAGS_TRAP in self._flags

	def issyscall(self):
		'''
		   Is the operand used as an index into the syscall table?
		'''
		return self.FLAGS_SYSCALL in self._flags

	def r(self):
		return self._access & self.ACCESS_R

	def w(self):
		return self._access & self.ACCESS_W

	def x(self):
		return self._access & self.ACCESS_X

	def seg_reg(self):
		'''
		   return the segment register applied to the operand,
		   if appropriate
		'''
		return self._segreg
	
	def to_address(self, vm=None):
		'''
		   return the operand as an address. If operand is
		   absolute or immediate, its value is returned. If
		   operand is relative, its value is added to
		   current addr and returned. otherwise, the BGVirtualMachine
		   object vm is called to resolved the address.
		'''
		return None

	#----------------------------------------------------------------------
	# lists and sets for convenience
	# the sets are used to replace value testing, e.g.
	# 	read_operands = insn.operands & bgo.operands.R
	# 	imlicit_operands = insn.operands & bgo.operands.I
	
	# sets of operand flag types: these can be differenced with 
	# the Instruction.operands set
	# I : set of all implicit operands
	I = set.Set(expr=lambda x: self.FLAGS_IMPLICIT in x.flags)
	# E : set of all explicit operands
	E = set.Set(expr=lambda x: self.FLAGS_IMPLICIT not in x.flags)
	
	# convenience variable for invalid address compares
	INVALID_ADDR = None
	
	# operand access type values
	ACCESS_R  = 0x01
	ACCESS_W = 0x02
	ACCESS_X  = 0x04
	
	# operand register type values
	REG_GENERAL = "general"
	REG_IN = "input"
	REG_OUT = "output"
	REG_LOCAL = "local"
	REG_FPU = "fpu"
	REG_SEG = "segment"
	REG_SIMD = "simd"
	REG_SYS = "system"
	REG_SP = "stack pointer"
	REG_FP = "frame pointer"
	REG_PC = "program counter"
	REG_RETADDR = "return addr"
	REG_CC = "condition code"
	REG_ZERO = "zero"
	REG_RET = "return value"
	REG_STRSRC = "string source"
	REG_STRDEST = "string dest"
	REG_COUNTER = "counter"
	REG_UNKNOWN = "unknown"
	
	register_types = ( REG_GENERAL, REG_IN, REG_OUT, REG_LOCAL, REG_FPU,
			   REG_SEG, REG_SIMD, REG_SYS, REG_SP, REG_FP, REG_PC,
			   REG_RETADDR, REG_CC, REG_ZERO, REG_RET, REG_STRSRC,
			   REG_STRDEST, REG_COUNTER, REG_UNKNOWN )
	
	# operand type values
	TYPE_UNUSED = ("unused", 0)
	TYPE_UNK = ("Unknown", 1)
	TYPE_REG = ("Register", 2)
	TYPE_IMM = ("Immediate", 3)
	TYPE_RELNEAR = ("RelativeNear", 4)
	TYPE_RELFAR = ("RelativeFar", 5)
	TYPE_ABSOLUTE = ("Absolute", 6)
	TYPE_OFFSET = ("Offset", 7)
	TYPE_BIT = ("Bit", 8)
	TYPE_EXPR = ("EffectiveAddress", 9)
	
	types = ( TYPE_UNUSED, TYPE_REG, TYPE_IMM, TYPE_RELNEAR, TYPE_RELFAR,
		  TYPE_ABSOLUTE, TYPE_EXPR, TYPE_OFFSET, TYPE_BIT, TYPE_UNK )
	
	# operand datatype values
	# the ID numbers are from the DB; disasm modules can define their own
	# encoding: (name, DB id, size in bytes)
	DATATYPE_UNKNOWN = ("unknown", 1, 1)
	DATATYPE_BYTE = ("byte", 2, 1)
	DATATYPE_HWORD = ("hword", 3, 2)
	DATATYPE_WORD = ("word", 4, 4)
	DATATYPE_DWORD = ("dword", 5, 8)
	DATATYPE_QWORD = ("qword", 6, 16)
	DATATYPE_DQWORD = ("dqword", 7, 32)
	DATATYPE_SREAL = ("single real", 8, 4)
	DATATYPE_DREAL = ("double real", 9, 8)
	DATATYPE_EXTREAL = ("extended real", 10, 10)
	DATATYPE_BCD = ("binary coded decimal", 11, 10)
	DATATYPE_SSIMD = ("packed single simd", 12, 16)
	DATATYPE_DSIMD = ("packed double simd", 13, 16)
	DATATYPE_SSSIMD = ("scalar single simd", 14, 4)
	DATATYPE_SDSIMD = ("scalar double simd", 15, 8)
	DATATYPE_DESC16 = ("descriptor 16", 16, 4)
	DATATYPE_DESC32 = ("descriptor 32", 17, 6)
	DATATYPE_PDESC16 = ("psuedo descriptor 16", 18, 6)
	DATATYPE_PDESC32 = ("psuedo descriptor 32", 19, 6)
	DATATYPE_FPUENV = ("fpu environment", 20, 28)
	DATATYPE_FPUREGS = ("fpu simd register state", 21, 512)
	
	data_types = ( DATATYPE_BYTE, DATATYPE_HWORD, DATATYPE_WORD, 
		DATATYPE_DWORD, DATATYPE_QWORD, DATATYPE_DQWORD, 
		DATATYPE_SREAL, DATATYPE_DREAL, DATATYPE_EXTREAL, 
		DATATYPE_BCD, DATATYPE_SSIMD, DATATYPE_DSIMD, 
		DATATYPE_SSSIMD, DATATYPE_SDSIMD, DATATYPE_DESC32, 
		DATATYPE_DESC16, DATATYPE_PDESC32, DATATYPE_PDESC16, 
		DATATYPE_FPUENV, DATATYPE_FPUREGS, DATATYPE_UNKNOWN )
	
	# operand flag values
	FLAGS_SIGN = "signed"
	FLAGS_STR = "string"
	FLAGS_CONST = "constant"
	FLAGS_PTR = "pointer"
	FLAGS_TRAP = "trap"
	FLAGS_SYSCALL = "syscall"
	FLAGS_IMPLICIT = "implied"
	FLAGS_HARDCODE = "hardcoded"
	
	flag_types = ( FLAGS_SIGN, FLAGS_STR, FLAGS_CONST, FLAGS_PTR, 
		       FLAGS_TRAP, FLAGS_SYSCALL, FLAGS_IMPLICIT, 
		       FLAGS_HARDCODE )
	
	# sets of operand access types
	# R : set of all read operands
	R = set.Set(expr=lambda x: x.access & ACCESS_R)
	# W : set of all write operands
	W = set.Set(expr=lambda x: x.access & ACCESS_W)
	# X : set of all execute operands
	X = set.Set(expr=lambda x: x.access & ACCESS_X)
	
	# sets of operand types
	# Reg : set of all register operands
	Reg = set.Set(expr=lambda x: x.type == TYPE_REG)
	# Imm : set of all imediate operands
	Imm = set.Set(expr=lambda x: x.type == TYPE_IMM)
	# Mem : set of all memory operands
	Mem = set.Set(expr=lambda x: x.type in (TYPE_RELNEAR, TYPE_RELFAR, 
	              TYPE_ABSOLUTE, TYPE_EXPR, TYPE_OFFSET) )
	
#-------------------------------------------------------------------------
# Operand types

class Relative(Operand):
	def __init__(self, insn, order, type=None, val=0, offset=0, address=0):
		if type is None:
			type = self.TYPE_RELNEAR
		Operand.__init__(self, insn, order, type)
		self._type = type	# type is TYPE_RELNEAR or TYPE_RELFAR
		self._value = val
		self._offset = offset
		self._address = address

	def __str__(self):
		buf = "<operand type='RelativeFar'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"
		
		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"
		
		buf = buf + "<type>" + self.type() + "</type>\n"
		buf = buf + "<value>" + str(self._value) + "</value>\n"
		buf = buf + "<offset>" + str(self._offset) + "</offset>\n"
		buf = buf + "<address>" + str(self._address) + "</address>\n"
		buf = buf + "</operand>\n"

		return buf
	
	def __repr__(self):
		return self.__str__()

	def type(self):
		return self._type[0]

	def value(self):
		return self._value

	def address(self):
		return self._address
	
	def offset(self):	
		return self._offset

	def apply_constant(self, constant):
		pass

	def remove_constant(self):
		pass

	def to_address(self, vm=None):
		return self._address

class ImmValue(object):
	'''
	   The immediate value encoded in an operand. Given its own
	   class so that immediate values can be replaced with symbolic
	   constants in Immediate and Expression operands.
	'''
	def __init__(self, value=0):
		self._value = value

	def value(self):
		return self._value

	def constant(self):
		return None

	def __str__(self):
		return str(self._value)

	def __repr__(self):
		return str(self._value)

class ImmAddress(ImmValue):
	'''
	   An ImmValue which uses hex() instead of str() in __str__
	'''
	def __init__(self, value=0):
		ImmValue.__init__(self, value)

	def __str__(self):
		return hex(self._value)

	def __repr__(self):
		return hex(self._value)

class ImmConstant(object):
	'''
	   An immediate value associated with a symblic constant.
	   Replaces the ImmValue in an Operand object.
	   A Constant must be a subclass of the BGO constant object
	'''
	def __init__(self, constant):
		self._constant = constant

	def value(self):
		return self._constant.value()

	def constant(self):
		return self._constant

	def __str__(self):
		return self._constant.name()

	def __repr__(self):
		namespace = self._constant.namespace()
		if namespace != "":
			buf = namespace + '.'
		else:
			buf = ''
		buf + self._constant.name()

class Immediate(Operand):
	def __init__(self, insn, order, val=None):
		Operand.__init__(self, insn, order, type=self.TYPE_IMM)
		self._imm = ImmValue(val)

	def __str__(self):
		buf = "<operand type='Immediate'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		buf = buf + "<val>" + hex(self._imm.value()) + "</val>\n"
		buf = buf + "</operand>\n"

		return buf
	
	def __repr__(self):
		return self.__str__()

	def value( self ):
		return self._imm.value()

	def apply_constant(self, constant):
		'''
		   Associate symbolic constant object with operand
		'''
		if self.value() != constant.value():
			raise AssertionError, 'Constant does not match value'

		self._imm = ImmConstant(constant)
	
	def constant(self):
		'''
		   Return the symbolic constant associted with the value,
		   or None.
		'''
		return self._imm.constant()

	def remove_constant(self):
		self._imm = ImmValue(self._imm.value())

	def to_address(self, vm=None):
		return self._imm.value()

class Offset(Immediate):
	def __init__(self, insn, order, val=0):
		Operand.__init__(self, insn, order, self.TYPE_OFFSET)
		if -256 < val < 256:
			# if this is a byte value, we treat it as a 
			# displacement ( a signed integer)
			self._imm = ImmValue(val)
		else:
			# otherwise we treated it as an address
			self._imm = ImmAddress(val)

	def __str__(self):
		buf = "<operand type='Offset'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		buf = buf + "<val>" + hex(self._imm.value()) + "</val>\n"
		buf = buf + "</operand>\n"

		return buf

	def remove_constant(self):
		val = self._imm.value()
		if -256 < val < 256:
			self._imm = ImmValue(val)
		else:
			self._imm = ImmAddress(val)

	def to_address(self, vm=None):
		# FIXME: is this correct? what if value < 256?
		#        add it to current_addr?
		return self._imm.value()

class Address(Immediate):
	def __init__(self, insn, order, val=None):
		Operand.__init__(self, insn, order, self.TYPE_ABSOLUTE)
		self._imm = ImmAddress(val)

	def __str__(self):
		buf = "<operand type='Address'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		buf = buf + "<val>" + hex(self._imm.value()) + "</val>\n"
		buf = buf + "</operand>\n"

		return buf

	def remove_constant(self):
		self._imm = ImmAddress(self._imm.value())

	def to_address(self, vm=None):
		return self._imm.value()


class CpuRegister(object):
	# helper class, so we can use registers outside of operands
	def __init__(self, id=None, mnemonic=None, type=None, size=None, \
				alias=None, alias_shift=0):
		# note: alias has to be a CpuRegister object already
		self._id = id
		self._mnemonic = mnemonic
		self._type = type
		self._size = size
		self._alias = alias
		self._alias_shift = alias_shift
		
		if self._type is None:
			self._type = []

	def __xml_str(self, recurse=False):
		buf = "<register>\n"

		buf = buf + "<id>" + str(self._id) + "</id>\n"
		buf = buf + "<mnemonic>" + str(self._mnemonic) + "</mnemonic>\n"
		buf = buf + "<size>" + str(self._size) + "</size>\n"

		for type in self._type:
			buf = buf + "<type>" + type + "</type>\n"

		if self._alias is not None:
			buf = buf + "<alias shift='" + \
				str(self._alias_shift) + "'>"
				
			if recurse:
				buf = buf + repr(self._alias)
			else:
				buf = buf + "(CpuRegister Instance)"
			buf = buf + "</alias>\n"

		buf = buf + "</register>\n"

		return buf
	
	def __str__(self):
		return self.__xml_str()

	def __repr__(self):
		return self.__xml_str(True)

	def id(self):
		return self._id

	def mnemonic(self):
		return self._mnemonic

	def type(self):
		return self._type
	
	def type_str(self):
		str = ''
		
		for t in self._type:
			if str == '':
				str = t
			else:
				str = str + '|' + t
		
		return str

	def size(self):
		return self._size

	def alias(self):
		return self._alias
	
	def alias_shift(self):
		return self._alias_shift
	

class EffectiveAddress(Operand):
	EADDR_DISP='disp'
	EADDR_BASE='base'
	EADDR_INDEX='index'

	def __init__(self, insn, order, disp=None, base=None, index=None, \
				 scale=None):
		# Note: base and index must be CpuRegister objects already!
		Operand.__init__(self, insn, order, self.TYPE_EXPR)
		self._base = base
		self._index = index
		self._scale = scale

		# disp is an offset -- see Offset class for explanation
		if -256 < disp < 256:
			self._disp = ImmValue(disp)
		else:
			self._disp = ImmAddress(disp)


	def __xml_str(self, recurse=False):
		buf = "<operand type='EffectiveAddess'>\n" + \
			"<order>" + str(self._order) + "</order>\n" +\
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		if self._base is not None:
			buf = buf + "<base>"
			if recurse:
				buf = buf + repr(self._base)
			else:
				buf = buf + str(self._base)
			buf = buf + "</base>\n"

		if self._index is not None:
			buf = buf + "<index>"
			if recurse:
				buf = buf + repr(self._index)
			else:
				buf = buf + str(self._index)
			buf = buf + "</index>\n"

		if self._scale is not None:
			buf = buf + "<scale>" + str(self._scale) + "</scale>\n"

		if self._disp is not None:	
			buf = buf + "<disp>" + hex(self._disp.value()) + \
				"</disp>\n"

		buf = buf + "</operand>\n"
		
		return buf
	
	def __str__(self):
		return self.__xml_str()

	def __repr__(self):
		return self.__xml_str(True)

	def disp( self ):
		return self._disp.value()

	def base( self ):
		return self._base

	def index( self ):
		return self._index

	def scale( self ):
		return self._scale

	def apply_constant(self, constant, to=EADDR_DISP):
		if to == EADDR_DISP:
			self._disp = ImmConstant(constant)
		elif to == EADDR_BASE:
			pass
		elif to == EADDR_INDEX:
			pass

	def constant(self, part=EADDR_DISP):
		if part == EADDR_DISP:
			return self._disp.constant()
		elif part == EADDR_BASE:
			pass
		elif part == EADDR_INDEX:
			pass

	def remove_constant(self, part=EADDR_DISP):
		if part == EADDR_DISP:
			disp = self._disp.value()
			if -256 < val < 256:
				self._disp = ImmValue(disp)
			else:
				self._disp = ImmAddress(disp)
		elif part == EADDR_BASE:
			pass
		elif part == EADDR_INDEX:
			pass

	def to_address(self, vm=None):
		if vm is not None:
			# TODO: write VM interface!
			pass

		return None


class Register(Operand):
	def __init__(self, insn, order, id=None, mnemonic=None, type=None, \
				 size=None, alias=None, alias_shift=0):
		Operand.__init__(self, insn, order, self.TYPE_REG)
		self._cpu_reg = CpuRegister(id, mnemonic, type, size, alias, 
			alias_shift)

	def __xml_str(self, recurse=False):
		buf = "<operand type='Register'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		if recurse:
			buf = buf + repr(self._cpu_reg)
		else:
			buf = buf + str(self._cpu_reg)

		buf = buf + "</operand>\n"

		return buf
	
	def __str__(self):
		return self.__xml_str()

	def __repr__(self):
		return self.__xml_str(True)

	def id(self):
		return self._cpu_reg.id()

	def mnemonic(self):
		return self._cpu_reg.mnemonic()

	def type(self):
		return self._cpu_reg.type()

	def type_str(self):
		return self._cpu_reg.type_str()

	def size(self):
		return self._cpu_reg.size()

	def alias(self):
		return self._cpu_reg.alias()

	def alias_shift(self):
		return self._cpu_reg.alias_shift()

	def apply_constant(self, constant):
		pass

	def remove_constant(self):
		pass

	def to_address(self, vm=None):
		if vm is not None:
			# TODO: write VM interface!
			pass
		return None

class Bit(Operand):
	''' 
	   a bit in another operand
	   e.g. a flag in the condition codes or flags register 
	   this is simply a convenience operand for set/clear opcodes
	'''
	def __init__(self, insn, order, position, mnemonic=None):
		Operand.__init__(self, insn, order, self.TYPE_BIT)
		self._bit_pos = position
		if mnemonic is None:
			mnemonic = 'bit' + str(position)
		self._mnemonic = mnemonic

	def __xml_str(self):
		buf = "<operand type='Bit'>\n" + \
			"<order>" + str(self._order) + "</order>\n" + \
			"<datatype>" + str(self.datatype()) + "</datatype>\n" +\
			"<access>" + hex(self._access) + "</access>\n"
			
		buf = buf + "<position>" + str(self.position()) + "</position>\n"
		buf = buf + "<mnemonic>" + self.mnemonic() + "</mnemonic>\n"
		buf = buf + "</operand>\n"
		
		return buf

	def mnemonic(self):
		return self._mnemonic
	
	def position(self):
		return self._bit_pos

	def __str__(self):
		return self.__xml_str()

	def __repr__(self):
		return self.__xml_str()

	def apply_constant(self, constant):
		pass

	def remove_constant(self):
		pass

	def to_address(self, vm=None):
		return None
