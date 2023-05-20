#!/usr/bin/python
'''
	Big O X86 Disassembler module
	Instruction Factory
'''

if __name__ == "__main__":
	# fix for running from top-level dir
	import sys
	sys.path.append(".")

import array			# for insn.bytes
import x86disasm as libdisasm

# --bgo-- 
import BGInstruction as instr	# big o instruction class
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
from disasm_modules.x86_Classes.x86Enum import *
from disasm_modules.x86_Classes.x86Insn import *


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
	cpu_map = {	libdisasm.cpu_8086: x86_module.cpu(CPU_8086),
			libdisasm.cpu_80286: 
				x86_module.cpu(CPU_80286),
			libdisasm.cpu_80386: 
				x86_module.cpu(CPU_80386),
			libdisasm.cpu_80387: 
				x86_module.cpu(CPU_80387),
			libdisasm.cpu_80486: 
				x86_module.cpu(CPU_80486),
			libdisasm.cpu_pentium: 
				x86_module.cpu(CPU_PENTIUM),
			libdisasm.cpu_pentiumpro: 
				x86_module.cpu(CPU_PENTIUMPRO),
			libdisasm.cpu_pentium2: 
				x86_module.cpu(CPU_PENTIUM2),
			libdisasm.cpu_pentium3: 
				x86_module.cpu(CPU_PENTIUM3),
			libdisasm.cpu_pentium4: 
				x86_module.cpu(CPU_PENTIUM4),
			libdisasm.cpu_k6: x86_module.cpu(CPU_K6),
			libdisasm.cpu_k7: x86_module.cpu(CPU_K7),
			libdisasm.cpu_athlon: 
				x86_module.cpu(CPU_ATHLON) }

	return cpu_map.get(insn.cpu, instr.Instruction.CPU_UNKNOWN)

#---------------------------------------------------------

def convert_isa(insn):
	isa_map = {	libdisasm.isa_gp: instr.Instruction.ISA_GP,
			libdisasm.isa_fp: instr.Instruction.ISA_FP,
			libdisasm.isa_fpumgt: 
				x86_module.isa(ISA_FPUMGT),
			libdisasm.isa_mmx: x86_module.isa(ISA_MMX),
			libdisasm.isa_sse1: x86_module.isa(ISA_SSE1),
			libdisasm.isa_sse2: x86_module.isa(ISA_SSE2),
			libdisasm.isa_sse3: x86_module.isa(ISA_SSE3),
			libdisasm.isa_3dnow: 
				x86_module.isa(ISA_3DNOW),
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
	op._op_def_id = _bitops[val]

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
		(flag_factory,(Bit.Clear, EFLAG_CARRY)),
	libdisasm.insn_clear_zero : 
		(flag_factory,(Bit.Clear, EFLAG_ZERO) ),
	libdisasm.insn_clear_oflow : 
		(flag_factory,(Bit.Clear, EFLAG_OFLOW)),
	libdisasm.insn_clear_dir : 
		(flag_factory,(Bit.Clear, EFLAG_DIR) ),
	libdisasm.insn_clear_sign : 
		(flag_factory,(Bit.Clear, EFLAG_SIGN)),
	libdisasm.insn_clear_parity : 
		(flag_factory,(Bit.Clear, EFLAG_PARITY)), 
	libdisasm.insn_set_carry : 
		(flag_factory,(Bit.Set, EFLAG_CARRY)),
	libdisasm.insn_set_zero :
		(flag_factory,(Bit.Set, EFLAG_ZERO) ),
	libdisasm.insn_set_oflow :
		(flag_factory,(Bit.Set, EFLAG_OFLOW)),
	libdisasm.insn_set_dir : 
		(flag_factory,(Bit.Set, EFLAG_DIR) ),
	libdisasm.insn_set_sign :
		(flag_factory,(Bit.Set, EFLAG_SIGN)),
	libdisasm.insn_set_parity : 
		(flag_factory,(Bit.Set, EFLAG_PARITY) ),
	libdisasm.insn_tog_carry : 
		(flag_factory,(Bit.Toggle, EFLAG_CARRY)),
	libdisasm.insn_tog_zero :
		(flag_factory,(Bit.Toggle, EFLAG_ZERO) ),
	libdisasm.insn_tog_oflow :
		(flag_factory,(Bit.Toggle, EFLAG_OFLOW)),
	libdisasm.insn_tog_dir : 
		(flag_factory,(Bit.Toggle, EFLAG_DIR) ),
	libdisasm.insn_tog_sign : 
		(flag_factory,(Bit.Toggle, EFLAG_SIGN)),
	libdisasm.insn_tog_parity : 
		(flag_factory,(Bit.Toggle, EFLAG_PARITY)), 
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
		(load_factory, (LodStor.Move, CONST_PI)),
	libdisasm.insn_fldz : 
		(load_factory, (LodStor.Move, CONST_ZERO)),
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

