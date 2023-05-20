#!/usr/bin/python
'''
	Base Disassembler virtual class
'''
#-------------------------------------------------------------------------
# Disassembler

# --bgo--

class Disasm(object):
	def __init__(self, options=0):
		# This can be implemented by cpu modules
		self._options = options
		self._name = "Virtual"

	def disasm_address(self, disasm_buf, offset=0):
		# This is implemented by cpu modules
		raise NotImplementedError, 'disasm_address is virtual'

	def disasm_range(self, disasm_buf, offset=0, len=0, fn=None, 
			 until=None):
		'''
		   Disassemble all bytes in DisasmBuffer disasm_buf,
		   from offset to offset + len.
		   Call fn for each instruction disassembled.
		   If callabale 'until' is provided, it is applied to
		      each instruction at the tail of the disassembly loop;
		      when it evaluates True this function returns.
		'''
		if len == 0:
			len = disasm_buf.size()
		pos = offset
		while pos < len:
			# if instruction has been disasmed, skip to next addr
			rva = disasm_buf.offset_to_rva(pos)
			if disasm_buf.seen_address(rva):
				i = disasm_buf.instructions(rva)
				pos += i.size()
				continue
			
			i = self.disasm_address(disasm_buf, pos)
			if i is None:
				raise AssertionError, \
					self._name + " returned insn: None"
			
			# invoke callback
			if fn is not None and callable(fn):
				fn(i)
			
			# add to list of instructions in disasm_buf
			disasm_buf.add_insn(i)
			
			if i.size() == 0:
				# for debugging: instruction size should
				# never be zero, even if it is invalid
				raise AssertionError, "Insn size 0: " + \
					i.mnemonic()
			if until is not None and iscallable(until) and until(i):
				return

			pos += i.size()

	def disasm_forward(self, disasm_buf, offset=0, until=None):
		'''
		   If callabale 'until' is provided, it is applied to
		      each instruction at the tail of the disassembly loop;
		      when it evaluates True this function returns.
		'''
		pass

	def disasm_invariant(self, disasm_buf, offset=0):
		'''
		   Disassemble an instruction and return an invariant 
		   representation
		'''
		# This is implemented by cpu modules
		raise NotImplementedError, 'disasm_invariant is virtual'

	def disasm_size(self, disasm_buf, offset=0):
		'''
		   Disassemble a single instruction and return only its
		   size
		'''
		if offset > disasm_buf.size():
			return 0
		i = self.disasm_address(disasm_buf, offset)

		return i.size()

