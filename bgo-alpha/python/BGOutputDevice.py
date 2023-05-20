#!/usr/bin/python

'''
	BGO Output Format class
'''

import BGAssembler as assembler
import BGSyntax as syntax

default_asm = assembler.default_assembler()
default_syn = syntax.default_syntax()

class Output(object):
	def __init__(self):
		pass
	
	def file(self, file, asm=default_asm, syn=default_syn):
		# print file header
		str = ''
		
		# for each section, do section
		# print file footer
		pass
	
	def section(self, sec, asm=default_asm, syn=default_syn):
		# print section header
		str = ''
		str = str + self.disasm_buf( sec, asm, syn)
		# print section footer
		pass
	
	def disasm_buf(self, buf, asm=default_asm, syn=default_syn):
		# print header
		str = ''
		
		prev_addr = buf.load_addr()
		prev_size = 0
		
		for i in buf.instructions:
			if i.address() < (prev_addr + prev_size):
				pass
			
			# if function entry...
			
			str = str + self.instruction(i, asm, syntax)
			
			# if function exit
			
			prev_addr = i.address()
			prev_size = i.size()
		
		end_addr = buf.load_addr() + buf.size()
		while prev_addr + prev_size < end_addr:
			# check for data at end of segment
			pass
		
		# print footer
		return str
	
	def instruction(self, insn, asm=default_asm, syn=default_syn):
		# hand off to assembler
		str = ''
		# if label:
		str = str + asm.instruction(insn, syn, self)
		# if xrefs:
		return str
	
	def operand(self, insn, asm=default_asm, syn=default_syn):
		# hand off to assembler
		return asm.operand(insn, syn, self)
	
	def set_color(self, color):
		pass
	
	def set_font(self, font):
		# set font and size
		pass
	
	def set_style(self, style):
		pass
	
	COLOR_ = ''
	STYLE_ = ''
