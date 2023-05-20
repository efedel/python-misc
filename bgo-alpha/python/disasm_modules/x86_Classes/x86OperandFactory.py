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

import x86disasm as libdisasm
# --bgo-- 
import BGOperand as operand	# big o operand class
import utils.set as set

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
