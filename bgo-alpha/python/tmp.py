		if insn.group == x86disasm.insn_controlflow:
			return "Control Flow"
		if insn.group == x86disasm.insn_arithmetic:
			return "Arithmetic"
		if insn.group == x86disasm.insn_logic:
			return "Logical"
		if insn.group == x86disasm.insn_stack:
			return "Stack"
		if insn.group == x86disasm.insn_comparison:
			return "Compare"
		if insn.group == x86disasm.insn_move:
			return "Move"
		if insn.group == x86disasm.insn_string:
			return "String"
		if insn.group == x86disasm.insn_bit_manip:
			return "Bit Manipulation"
		if insn.group == x86disasm.insn_flag_manip:
			return "Flag Manipulation"
		if insn.group == x86disasm.insn_fpu:
			return "Floating Point"
		if insn.group == x86disasm.insn_interrupt:
			return "Trap"
		if insn.group == x86disasm.insn_system:
			return "System"
		if insn.group == x86disasm.insn_other:
			return "Other"
		return "None"
		if insn.type == x86disasm.insn_jmp :
			return "jump"
		if insn.type == x86disasm.insn_jcc :
			return "cond jump"
		if insn.type == x86disasm.insn_call :
			return "call"
		if insn.type == x86disasm.insn_callcc :
			return "cond call"
		if insn.type == x86disasm.insn_return :
			return "return"
		if insn.type == x86disasm.insn_add :
			return "add"
		if insn.type == x86disasm.insn_sub :
			return "sub"
		if insn.type == x86disasm.insn_mul :
			return "mul"
		if insn.type == x86disasm.insn_div :
			return "div"
		if insn.type == x86disasm.insn_inc :
			return "inc"
		if insn.type == x86disasm.insn_dec :
			return "dec"
		if insn.type == x86disasm.insn_shl :
			return "shift l"
		if insn.type == x86disasm.insn_shr :
			return "shift r"
		if insn.type == x86disasm.insn_rol :
			return "rot l"
		if insn.type == x86disasm.insn_ror :
			return "rot r"
		if insn.type == x86disasm.insn_and :
			return "and"
		if insn.type == x86disasm.insn_or :
			return "or"
		if insn.type == x86disasm.insn_xor :
			return "xor"
		if insn.type == x86disasm.insn_not :
			return "not"
		if insn.type == x86disasm.insn_neg :
			return "neg"
		if insn.type == x86disasm.insn_push :
			return "push"
		if insn.type == x86disasm.insn_pop :
			return "pop"
		if insn.type == x86disasm.insn_pushregs :
			return "push regs"
		if insn.type == x86disasm.insn_popregs :
			return "pop regs"
		if insn.type == x86disasm.insn_pushflags :
			return "push flags"
		if insn.type == x86disasm.insn_popflags :
			return "pop flags"
		if insn.type == x86disasm.insn_enter :
			return "enter frame"
		if insn.type == x86disasm.insn_leave :
			return "leave frame"
		if insn.type == x86disasm.insn_test :
			return "test"
		if insn.type == x86disasm.insn_cmp :
			return "cmp"
		if insn.type == x86disasm.insn_mov :
			return "move"
		if insn.type == x86disasm.insn_movcc :
			return "cond move"
		if insn.type == x86disasm.insn_xchg :
			return "xchng"
		if insn.type == x86disasm.insn_xchgcc :
			return "cond xchg"
		if insn.type == x86disasm.insn_strcmp :
			return "strcmp"
		if insn.type == x86disasm.insn_strload :
			return "load str"
		if insn.type == x86disasm.insn_strmov :
			return "move str"
		if insn.type == x86disasm.insn_strstore :
			return "store str"
		if insn.type == x86disasm.insn_translate :
			return "xlat"
		if insn.type == x86disasm.insn_bittest :
			return "bit test"
		if insn.type == x86disasm.insn_bitset :
			return "bit set"
		if insn.type == x86disasm.insn_bitclear :
			return "bit clr"
		if insn.type == x86disasm.insn_clear_carry :
			return "cf clr"
		if insn.type == x86disasm.insn_clear_zero :
			return "zf clr"
		if insn.type == x86disasm.insn_clear_oflow :
			return "of clr"
		if insn.type == x86disasm.insn_clear_dir :
			return "df clr"
		if insn.type == x86disasm.insn_clear_sign :
			return "sf clr"
		if insn.type == x86disasm.insn_clear_parity :
			return "pf clr"
		if insn.type == x86disasm.insn_set_carry :
			return "cf set"
		if insn.type == x86disasm.insn_set_zero :
			return "zf set"
		if insn.type == x86disasm.insn_set_oflow :
			return "of set"
		if insn.type == x86disasm.insn_set_dir :
			return "df set"
		if insn.type == x86disasm.insn_set_sign :
			return "sf set"
		if insn.type == x86disasm.insn_set_parity :
			return "pf set"
		if insn.type == x86disasm.insn_tog_carry :
			return "cf tog"
		if insn.type == x86disasm.insn_tog_zero :
			return "zf tog"
		if insn.type == x86disasm.insn_tog_oflow :
			return "of tog"
		if insn.type == x86disasm.insn_tog_dir :
			return "df tog"
		if insn.type == x86disasm.insn_tog_sign :
			return "sf tog"
		if insn.type == x86disasm.insn_tog_parity :
			return "pf tog"
		if insn.type == x86disasm.insn_fmov :
			return "move fp"
		if insn.type == x86disasm.insn_fmovcc :
			return "cond move fp"
		if insn.type == x86disasm.insn_fneg :
			return "neg fp"
		if insn.type == x86disasm.insn_fabs :
			return "abs fp"
		if insn.type == x86disasm.insn_fadd :
			return "add fp"
		if insn.type == x86disasm.insn_fsub :
			return "sub fp"
		if insn.type == x86disasm.insn_fmul :
			return "mul fp"
		if insn.type == x86disasm.insn_fdiv :
			return "div fp"
		if insn.type == x86disasm.insn_fsqrt :
			return "sqrt fp"
		if insn.type == x86disasm.insn_fcmp :
			return "cmp fp"
		if insn.type == x86disasm.insn_fcos :
			return "cos fp"
		if insn.type == x86disasm.insn_fldpi :
			return "ldpi fp"
		if insn.type == x86disasm.insn_fldz :
			return "ldz fp"
		if insn.type == x86disasm.insn_ftan :
			return "tan fp"
		if insn.type == x86disasm.insn_fsine :
			return "sine fp"
		if insn.type == x86disasm.insn_fsys :
			return "sys fp"
		if insn.type == x86disasm.insn_int :
			return "trap"
		if insn.type == x86disasm.insn_intcc :
			return "cond trap"
		if insn.type == x86disasm.insn_iret :
			return "trap ret"
		if insn.type == x86disasm.insn_bound :
			return "bound trap"
		if insn.type == x86disasm.insn_debug :
			return "debug trap"
		if insn.type == x86disasm.insn_trace :
			return "trace trap"
		if insn.type == x86disasm.insn_invalid_op :
			return "invop trap"
		if insn.type == x86disasm.insn_oflow :
			return "oflow trap"
		if insn.type == x86disasm.insn_halt :
			return "halt"
		if insn.type == x86disasm.insn_in :
			return "port in"
		if insn.type == x86disasm.insn_out :
			return "port out"
		if insn.type == x86disasm.insn_cpuid :
			return "cpuid"
		if insn.type == x86disasm.insn_nop :
			return "nop"
		if insn.type == x86disasm.insn_bcdconv :
			return "conv bcd"
		if insn.type == x86disasm.insn_szconv :
			return "conv size"
		return "invalid"
		if insn.cpu == x86disasm.cpu_8086:
			return "8086"
		if insn.cpu == x86disasm.cpu_80286:
			return "80286"
		if insn.cpu == x86disasm.cpu_80386:
			return "80386"
		if insn.cpu == x86disasm.cpu_80387:
			return "80387"
		if insn.cpu == x86disasm.cpu_80486:
			return "80486"
		if insn.cpu == x86disasm.cpu_pentium:
			return "Pentium"
		if insn.cpu == x86disasm.cpu_pentiumpro:
			return "Pentium Pro"
		if insn.cpu == x86disasm.cpu_pentium2:
			return "Pentium 2"
		if insn.cpu == x86disasm.cpu_pentium3:
			return "Pentium 3"
		if insn.cpu == x86disasm.cpu_pentium4:
			return "Pentium 4"
		if insn.cpu == x86disasm.cpu_k6:
			return "K6"
		if insn.cpu == x86disasm.cpu_k7:
			return "K7"
		if insn.cpu == x86disasm.cpu_athlon:
			return "Athlon"
		if insn.isa == x86disasm.isa_gp:
			return "General Purpose"
		if insn.isa == x86disasm.isa_fp:
			return "Floating Point"
		if insn.isa == x86disasm.isa_fpumgt:
			return "FPU/SIMD Management"
		if insn.isa == x86disasm.isa_mmx:
			return "MMX"
		if insn.isa == x86disasm.isa_sse1:
			return "SSE"
		if insn.isa == x86disasm.isa_sse2:
			return "SSE 2"
		if insn.isa == x86disasm.isa_sse3:
			return "SSE 3"
		if insn.isa == x86disasm.isa_3dnow:
			return "3D Now"
		if insn.isa == x86disasm.isa_sys:
			return "System"
		if insn.prefixes & x86disasm.insn_rep_zero:
			prefixes.append("repz")
		if insn.prefixes & x86disasm.insn_rep_notzero:
			prefixes.append("repnz")
		if insn.prefixes & x86disasm.insn_lock:
			prefixes.append("lock")
		if insn.note & x86disasm.insn_note_ring0:
			notes.append("ring0")
		if insn.note & x86disasm.insn_note_smm:
			notes.append("smm")
		if insn.note & x86disasm.insn_note_serial:
			notes.append("serializing")
		if insn.flags_set & x86disasm.insn_carry_set:
			results.append("cf set")
		if insn.flags_set & x86disasm.insn_zero_set:
			results.append("zf set")
		if insn.flags_set & x86disasm.insn_oflow_set:
			results.append("of set")
		if insn.flags_set & x86disasm.insn_dir_set:
			results.append("df set")
		if insn.flags_set & x86disasm.insn_sign_set:
			results.append("sf set")
		if insn.flags_set & x86disasm.insn_parity_set:
			results.append("pf set")
		if insn.flags_set & x86disasm.insn_carry_clear:
			results.append("cf clr")
		if insn.flags_set & x86disasm.insn_zero_clear:
			results.append("zf clr")
		if insn.flags_set & x86disasm.insn_oflow_clear:
			results.append("of clr")
		if insn.flags_set & x86disasm.insn_dir_clear:
			results.append("df clr")
		if insn.flags_set & x86disasm.insn_sign_clear:
			results.append("sf clr")
		if insn.flags_set & x86disasm.insn_parity_clear:
			results.append("pf clr")
		if insn.flags_tested & x86disasm.insn_carry_set:
			results.append("cf")
		if insn.flags_tested & x86disasm.insn_zero_set:
			results.append("zf")
		if insn.flags_tested & x86disasm.insn_oflow_set:
			results.append("of")
		if insn.flags_tested & x86disasm.insn_dir_set:
			results.append("df")
		if insn.flags_tested & x86disasm.insn_sign_set:
			results.append("sf")
		if insn.flags_tested & x86disasm.insn_parity_set:
			results.append("pf")
		if insn.flags_tested & x86disasm.insn_carry_or_zero_set:
			results.append("cf || zf")
		if insn.flags_tested & x86disasm.insn_zero_set_or_sign_ne_oflow:
			results.append("zf || sf != of")
		if insn.flags_tested & x86disasm.insn_carry_clear:
			results.append("! cf")
		if insn.flags_tested & x86disasm.insn_zero_clear:
			results.append("! zf")
		if insn.flags_tested & x86disasm.insn_oflow_clear:
			results.append("! of")
		if insn.flags_tested & x86disasm.insn_dir_clear:
			results.append("! df")
		if insn.flags_tested & x86disasm.insn_sign_clear:
			results.append("! sf")
		if insn.flags_tested & x86disasm.insn_parity_clear:
			results.append("! pf")
		if insn.flags_tested & x86disasm.insn_sign_eq_oflow:
			results.append("sf == of")
		if insn.flags_tested & x86disasm.insn_sign_ne_oflow:
			results.append("sf != of")

