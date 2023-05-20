#!/usr/bin/python
'''
	Big O Intel Assembler module
'''

# --bgo--
import BGAssembler

class IntelAssembler(assembler.Assembler):
	def __init__(self, options=""):
		self._name = 'Intel'
		self._options = options
	
	def formats(self):
		return ('text', 'html', 'xml')

	def file(self, file, format='xml'):
		str = ''
		return str
	
	def disasm_buffer(self, buf, format='text'):
		str = ''
		for i in buf.instructions():
			pass
		
		return str

	def section(self, section, format='text'):
		str = ''
		return str
	
	def instruction(self, insn, format='text'):
		str = ''
		return str
	
	def operand(self, op, format='text'):
		str = ''
		return str
	
	def data(self, data, format='text'):
		str = ''
		return str

if __name__ == '__main__':
	pass
