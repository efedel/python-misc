#!/usr/bin/python

'''
	Base Block class
'''

class Block(object):
	'''
	   A sequence of instructions, e.g. between { and } in C.

	   Methods:
	   	add_insn
		instructions : iterator
		blocks	: iterator

	   Members:
	   	__instructions (list)
		__blocks (list)
	'''

	def __init__(self):

		pass

	def add_insn(self):
		pass

	def instructions(self):
		pass

	def blocks(self):
		pass

	def __iter__(self):
		pass
