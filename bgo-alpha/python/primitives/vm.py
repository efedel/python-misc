#!/usr/bin/python

'''
	Virtual Machine class
'''

class VirtualMachine(object):
	
	def __init__(self):
		pass

	# machine management instructions
	def stack_push(self, val):
		pass
	def stack_pop(self):
		pass
	def heap_alloc(self, size):
		pass
	def head_free(self, ptr):
		pass
	def trap(self, trap_num):
		pass
	def reg_read(self, reg):
		pass
	def reg_write(self, reg, val):
		pass
	def mem_read(self, address):
		pass
	def mem_write(self, address, val):
		pass

	# address resolution for operand types
	def resolve_reg(self, reg):
		pass
	def resolve_eaddr(self, reg):
		pass

	# operations used by Instruction.eval()
	def op_add(self, a, b):
		pass
	def op_sub(self, a, b):
		pass
	def op_mul(self, a, b):
		pass
	def op_div(self, a, b):
		pass
	def op_shift(self, a, b):
		pass
	def op_and(self, a, b):
		pass
	def op_or(self, a, b):
		pass
	def op_xor(self, a, b):
		pass
	def op_neg(self, a):
		pass
	def flag_set(self, flag):
		pass
	def flag_clear(self, flag):
		pass
	def flag_test(self, flag):
		pass
	
