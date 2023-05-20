#!/usr/bin/python

'''
	BGO Syntax Highlighter class
'''

class Syntax(object):
	def __init__(self):
		_rule_types = {}
		self.add_rule_type('address')
		self.add_rule_type('cross ref')
		self.add_rule_type('symbol')
		self.add_rule_type('comment')
		self.add_rule_type('hex byte')
		self.add_rule_type('punctuation')
		self.add_rule_type('mnemonic')
		self.add_rule_type('operand')
		self.add_rule_type('string')
		self.add_rule_type('data type')
		self.add_rule_type('data object')
	
	def add_rule( self, type, rule ):
		''' rule is a callable, e.g. a lambda '''
		self._rule_types[type].append[rule]
	
	def add_rule_type( self, type ):
		self._rule_types[type] = []

'''
	Rules have the form :
		lambda op|insn|addr, output: 
'''
# lambda insn, outpuit:
# outpuit.set_style
# output.set_font
# outpuit.set_color
