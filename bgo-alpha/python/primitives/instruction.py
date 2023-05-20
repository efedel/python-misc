#!/usr/bin/python
'''
	Base Instruction Class
'''
import array
# --bgo--
import utils.set as set
import primitives.operand as operand

#-------------------------------------------------------------------------
# Instruction

class Instruction(object):
	'''
	   binary generic instruction
	'''

	def __doc__(self):
		pass

	def __init__(self, section=None):
		self._section = section
		self._operands = set.Set(get_key=lambda x: x._order)
		self._flags_set = []
		self._flags_tested = []
		self._bytes = []
		self._signature = []
		self._mnemonic = ""
		self._flags = []
		self._title = ""
		self._pseudocode = ""
		self._description = ""
		self._size = 0
		self._offset = 0
		self._address = 0
		self._prefixes = []
		self._prefix_mnemonic = ""
		self._major_type = self.GROUP_NONE
		self._minor_type = self.TYPE_INVALID
		self._cpu = self.CPU_UNKNOWN
		self._isa = self.ISA_UNKNOWN
		self._stack_mod = None
		
	# Instruction Interface
	# - Actions
	def add_operand(self, operand):
		num = len(self._operands) + 1
		operand.order = num
		self._operands.add(operand)

	def emulate(self):
		''' emulate this insn in vm '''
		pass

	def generic_asm(self):
		''' produce generic asm for this insn '''
		pass

	# - Access Members
	def offset(self):
		''' get offset of insn in section'''
		return self._offset
	
	def address(self):
		''' return load address/rva of insn'''
		return self._address

	def size(self):
		''' get size of instruction in bytes'''
		return self._size
	
	def next_address(self):
		''' 
		   return the load address of the next instruction.
		   this is used for control flow disasm; instructions
		   like JMP and RET override this to return None.
		'''
		return self.address() + self.size()

	def bytes(self):
		''' get bytes of insn: an array.array('B') '''
		return self._bytes
	
	def signature(self):
		''' 
		   get invariant bytes of insn
		   NOTE wildcard byte will be disasm-dependent!
		'''
		return self._signature
	
	def type(self):
		return self._major_type[0] + '|' + self._minor_type[0]

	def major(self):
		return self._major_type[0]
	
	def minor(self):
		print str(self._minor_type)
		print str(self._minor_type[0])
		return self._minor_type[0]

	def prefixes(self):
		''' get instruction prefixes '''
		return self._prefixes

	def prefix_str(self):
		''' get instruction prefixes in a |-delimited string '''
		prefixes = ''
		
		for p in self._prefixes:
			if prefixes == '':
				prefixes = p
			else:
				prefixes = prefixes + '|' + p

		return prefixes

	def prefix_mnemonic(self):
		''' get instruction prefix '''
		return self._prefix_mnemonic
	
	def mnemonic(self):
		''' get instruction mnemonic '''
		return self._mnemonic
	
	def flags_set(self):
		''' get flags set by instruction '''
		return self._flags_set

	def flags_set_str(self):
		''' get flags set by insn in a |-delimited string '''
		flags = ''
		
		for f in self._flags_set:
			if flags == '':
				flags = f
			else:
				flags = flags + '|' + f
		
		return flags
		
	def flags_tested(self):
		return self._flags_tested
		
	def flags_tested_str(self):
		''' get flags tested by insn in a |-delimited string '''
		flags = ''
		
		for f in self._flags_tested:
			if flags == '':
				flags = f
			else:
				flags = flags + '|' + f
		
		return flags

	def stack_mod(self):
		return self._stack_mod
	
	def cpu(self):
		''' get (minimum) CPU version of instruction '''
		return self._cpu[0]

	def isa(self):
		''' get instruction set (e.g. general, fpu) of insn '''
		return self._isa[0]

	def flags(self):
		''' get instruction flags, e.g. branch delay '''
		return self._flags

	def title(self):
		''' get full title of instruction '''
		return self._title

	def description(self):
		''' get opcode description of instruction '''
		return self._description

	def pseudocode(self):
		''' get psuedocode for instruction '''
		return self._pseudocode

	def section(self):
		''' get section object containing instruction '''
		return self._section

		# iterator over explicit operands ?

	def operands(self):
		''' return list of operands '''
		return self._operands

	def operand_count(self):
		''' return total number of operands '''
		return len(self._operands)

	def explicit_count(self):
		''' return number of explicit operands '''
		return len(self._operands & operand.E)

	def load_address(self):
		''' determine load addr based on section, i_address '''
		pass

	def file_offset(self):
		''' determine file offset based on section, i_offset '''
		pass

	def __xml_str(self, recurse=False):
		buf = "<instruction>\n";
		buf = buf + "<offset>" + hex(self._offset) + "</offset>\n"
		buf = buf + "<address>" + hex(self._address) + "</address>\n"
		buf = buf + "<size>" + str(self._size) + "</size>\n"
		
		buf = buf + "<bytes>"
		for b in array.array('B', self._bytes):
			buf = buf + hex(b) + ' '
		buf = buf + "</bytes>\n"
		
		buf = buf + "<major_type>" + self.major() + \
			"</major_type>\n"
		buf = buf + "<minor_type>" + self.minor() + \
			"</minor_type>\n"
		
		for p in self._prefixes:
			buf = buf + "<prefix>" + p + "</prefix>\n"
		
		if self._prefix_mnemonic != "":
			buf = buf + "<prefix_mnemonic>" + \
				self.prefix_mnemonic() + \
				"</prefix_mnemonic>\n"
		
		buf = buf + "<mnemonic>" + self.mnemonic() + "</mnemonic>\n"
		
		for o in self._operands:
			if recurse:
				buf = buf + repr(o)
			else:
				buf = buf + "<operand>(" + \
					o.type() + " Instance)</operand>\n"
				
		for f in self._flags_set:
			buf = buf + "<flag_set>" + f + "</flag_set>\n"

		for f in self._flags_tested:
			buf = buf + "<flag_tested>" + f + "</flag_tested>\n"

		for f in self._flags:
			buf = buf + "<flag>" + f + "</flag>\n"

		buf = buf + "<title>" + self.title() + "</title>"
		buf = buf + "<pseudocode>" + self.pseudocode() + \
			"</pseudocode>\n"
		buf = buf + "<description>" + self.description() + \
			"</description>\n"
		buf = buf + "<cpu>" + self.cpu() + "</cpu>\n"
		buf = buf + "<isa>" + self.isa() + "</isa>\n"

		if self._stack_mod is not None:
			buf = buf + "<stack_mod>" + str(self._stack_mod) + \
				"</stack_mod>\n"

		buf = buf + "</instruction>\n"
		return buf
	
	def __str__(self):
		return self.__xml_str()
	
	def __repr__(self):
		return self.__xml_str(True)
		
	def __hash__(self):
		return self._offset
	
	def __cmp__(self, insn):
		return self._offset - insn.offset()
	
	# -------- Major Type ----------
	# The IDs are from the DB
	GROUP_CONTROLFLOW = ("Control Flow",2)
	GROUP_ARITHMETIC = ("Arithmetic", 3)
	GROUP_LOGIC = ("Logical", 4)
	GROUP_STACK = ("Stack", 5)
	GROUP_COMPARE = ("Compare", 6)
	GROUP_LOADSTORE = ("Load/Store", 7)
	GROUP_BIT = ("Bit", 8)
	GROUP_TRAP = ("Trap", 9)
	GROUP_SYSTEM = ("System", 10)
	GROUP_MISC = ("Misc", 11)
	GROUP_NONE = ("None", 1)
	
	insn_groups = ( GROUP_CONTROLFLOW, GROUP_ARITHMETIC, GROUP_LOGIC, 
		GROUP_STACK, GROUP_COMPARE, GROUP_LOADSTORE, GROUP_BIT, 
		GROUP_TRAP, GROUP_SYSTEM, GROUP_MISC, GROUP_NONE )
	
	# -------- Minor Type ----------
	# control flow
	TYPE_JMP = ("jump", 2)
	TYPE_JCC = ("cond jump", 3)
	TYPE_CALL = ("call", 4)
	TYPE_CALLCC = ("cond call", 5)
	TYPE_RETURN = ("return", 6)
	# arithmetic
	TYPE_ADD = ("add", 7)
	TYPE_SUB = ("sub", 8)
	TYPE_MUL = ("mul", 9)
	TYPE_DIV = ("div", 10)
	TYPE_SHL = ("shift l", 13)
	TYPE_SHR = ("shift r", 14)
	TYPE_ABS = ("abs", 65)
	TYPE_SQRT = ("sqrt", 70)
	TYPE_COS = ("cos", 72)
	TYPE_TAN = ("tan", 75)
	TYPE_SINE = ("sine", 76)
	# logic
	TYPE_AND = ("and", 17)
	TYPE_OR = ("or", 18)
	TYPE_XOR = ("xor", 19)
	TYPE_NOT = ("not", 20)
	TYPE_NEG = ("neg", 21)
	# stack
	TYPE_PUSH = ("push", 22)
	TYPE_POP = ("pop", 23)
	TYPE_ENTER = ("enter frame", 28)
	TYPE_LEAVE = ("leave frame", 29)
	# compare
	TYPE_TEST = ("test", 30)
	TYPE_CMP = ("cmp", 31)
	# load/store
	TYPE_MOV = ("move", 32)
	TYPE_MOVCC = ("cond move", 33)
	TYPE_XCHG = ("xchng", 34)
	TYPE_XCHGCC = ("cond xchg", 35)
	# flag
	TYPE_CLEAR_BIT = ("bclear", 0)
	TYPE_SET_BIT = ("bset", 0)
	TYPE_TOG_BIT = ("btog", 0)
	# trap
	TYPE_TRAP = ("trap", 78)
	TYPE_TRAPCC = ("cond trap", 79)
	TYPE_TRET = ("trap ret", 80)
	TYPE_BOUND = ("bound trap", 81)
	TYPE_DEBUG = ("debug trap", 82)
	TYPE_TRACE = ("trace trap", 83)
	TYPE_INVALID_OP = ("invop trap", 84)
	TYPE_OFLOW = ("oflow trap", 85)
	# system
	TYPE_HALT = ("halt", 86)
	TYPE_IN = ("port in", 87)
	TYPE_OUT = ("port out", 88)
	TYPE_CPUID = ("cpuid", 89)
	TYPE_SYSCTL = ("sysctl", 0)
	# misc
	TYPE_NOP = ("nop", 90)
	TYPE_UNK = ("unknown", 91)
	TYPE_INVALID = ("invalid", 1)
	
	insn_types = ( TYPE_JMP, TYPE_JCC, TYPE_CALL, TYPE_CALLCC, TYPE_RETURN,
		TYPE_ADD, TYPE_SUB, TYPE_MUL, TYPE_DIV, TYPE_SHL, TYPE_SHR, 
		TYPE_ABS, TYPE_SQRT, TYPE_COS, TYPE_TAN, TYPE_SINE, 
		TYPE_AND, TYPE_OR, TYPE_XOR, TYPE_NOT, TYPE_NEG, 
		TYPE_PUSH, TYPE_POP, TYPE_ENTER, TYPE_LEAVE, 
		TYPE_TEST, TYPE_CMP, 
		TYPE_MOV, TYPE_MOVCC, TYPE_XCHG, TYPE_XCHGCC, 
		TYPE_CLEAR_BIT, TYPE_SET_BIT, TYPE_TOG_BIT, 
		TYPE_TRAP, TYPE_TRAPCC, TYPE_TRET, TYPE_BOUND, TYPE_DEBUG, 
		TYPE_TRACE, TYPE_INVALID_OP, TYPE_OFLOW, 
		TYPE_HALT, TYPE_IN, TYPE_OUT, TYPE_CPUID, 
		TYPE_NOP, TYPE_INVALID )

	# created by disasm
	#FLAG_CARRY = "cf"
	#FLAG_ZERO = "zf"
	#FLAG_OFLOW = "of"
	#FLAG_DIR = "df"
	#FLAG_SIGN = "sf"
	#FLAG_PARITY = "pf"


	# -------- CPU Architecture ----------
	CPU_UNKNOWN = ("UNKNOWN", 1)
	
	cpu_types = ( CPU_UNKNOWN, )
	
	# -------- Instruction Set ----------
	ISA_GP = ("General Purpose", 2)
	ISA_FP = ("Floating Point", 3)
	ISA_SYS = ("System", 4)
	ISA_UNKNOWN = ("UNKNOWN", 1)
	
	isa_types = ( ISA_GP, ISA_FP,ISA_SYS, ISA_UNKNOWN )
	
	# -------- Instruction Prefix ----------
	PREFIX_REP_ZERO = "repz"
	PREFIX_REP_NOTZERO = "repnz"
	PREFIX_LOCK = "lock"
	
	prefix_types = ( PREFIX_REP_ZERO, PREFIX_REP_NOTZERO, PREFIX_LOCK )
	
	# -------- Notes ----------
	NOTE_RING0 = "ring0"
	NOTE_SMM = "smm"
	NOTE_SERIAL = "serializing"
	NOTE_DELAY = "branch delay"
	
	note_types = ( NOTE_RING0, NOTE_SMM, NOTE_SERIAL, NOTE_DELAY )
	
	# -------- Flags/CC Set ----------
	FLAGS_SET_CARRY = "cf set"
	FLAGS_SET_ZERO = "zf set"
	FLAGS_SET_OFLOW = "of set"
	FLAGS_SET_DIR = "df set"
	FLAGS_SET_SIGN = "sf set"
	FLAGS_SET_PARITY = "pf set"
	FLAGS_CLEAR_CARRY = "cf clr"
	FLAGS_CLEAR_ZERO = "zf clr"
	FLAGS_CLEAR_OFLOW = "of clr"
	FLAGS_CLEAR_DIR = "df clr"
	FLAGS_CLEAR_SIGN = "sf clr"
	FLAGS_CLEAR_PARITY = "pf clr"
	
	flag_set_types = ( FLAGS_SET_CARRY, FLAGS_SET_ZERO, FLAGS_SET_OFLOW,
		FLAGS_SET_DIR, FLAGS_SET_SIGN, FLAGS_SET_PARITY, 
		FLAGS_CLEAR_CARRY, FLAGS_CLEAR_ZERO, FLAGS_CLEAR_OFLOW, 
		FLAGS_CLEAR_DIR, FLAGS_CLEAR_SIGN, FLAGS_CLEAR_PARITY )
	
	
	# -------- Flags/CC Tested ----------
	FLAGS_TEST_CARRY_SET = "cf"
	FLAGS_TEST_ZERO_SET = "zf"
	FLAGS_TEST_OFLOW_SET = "of"
	FLAGS_TEST_DIR_SET = "df"
	FLAGS_TEST_SIGN_SET = "sf"
	FLAGS_TEST_PARITY_SET = "pf"
	FLAGS_TEST_CARRY_OR_ZERO_SET = "cf || zf"
	FLAGS_TEST_ZERO_SET_OR_SIGN_NE_OFLOW = "zf || sf != of"
	FLAGS_TEST_CARRY_CLEAR = "! cf"
	FLAGS_TEST_ZERO_CLEAR = "! zf"
	FLAGS_TEST_OFLOW_CLEAR = "! of"
	FLAGS_TEST_DIR_CLEAR = "! df"
	FLAGS_TEST_SIGN_CLEAR = "! sf"
	FLAGS_TEST_PARITY_CLEAR = "! pf"
	FLAGS_TEST_SIGN_EQ_OFLOW = "sf == of"
	FLAGS_TEST_SIGN_NE_OFLOW = "sf != of"
	
	flag_test_types = ( FLAGS_TEST_CARRY_SET, FLAGS_TEST_ZERO_SET,
		FLAGS_TEST_OFLOW_SET, FLAGS_TEST_DIR_SET, FLAGS_TEST_SIGN_SET,
		FLAGS_TEST_PARITY_SET, FLAGS_TEST_CARRY_OR_ZERO_SET,
		FLAGS_TEST_ZERO_SET_OR_SIGN_NE_OFLOW, FLAGS_TEST_CARRY_CLEAR,
		FLAGS_TEST_ZERO_CLEAR, FLAGS_TEST_OFLOW_CLEAR, 
		FLAGS_TEST_DIR_CLEAR, FLAGS_TEST_SIGN_CLEAR, 
		FLAGS_TEST_PARITY_CLEAR, FLAGS_TEST_SIGN_EQ_OFLOW, 
		FLAGS_TEST_SIGN_NE_OFLOW )
	
