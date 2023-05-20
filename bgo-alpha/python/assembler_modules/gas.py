#!/usr/bin/python
'''
	Big O GNU as Assembler module
'''

# --bgo--
import BGAssembler

class gasAssembler(assemblerAssembler):
	def __init__(self, options="", colors=None):
		self._name = 'gas'
		self._options = options
		if colors:
			self._colors = colors
	
	def formats(self):
		return ('text', 'html', 'xml')

	def xml_file(self, file):
		pass
	def html_file(self, file):
		pass
	def text_file(self, file):
		pass

	def file(self, file, format='xml'):
		str = ''
		return str

	def xml_disasmbuf(self, buf):
		pass
	def html_disasmbuf(self, buf):
		pass
	def text_disasmbuf(self, buf):
		pass
	
	def disasm_buffer(self, buf, format='text'):
		str = ''
		for i in buf.instructions():
			pass
		
		return str

	def xml_section(self, sec):
		pass
	def html_section(self, sec):
		pass
	def text_section(self, sec):
		pass

	def section(self, section, format='text'):
		str = ''
		return str

	def xml_instruction(self, insn):
		pass
	def html_instruction(self, insn):
		pass
	def text_instruction(self, insn):
		pass

	def instruction(self, insn, format='text'):
		str = ''
		return str
	
	def xml_operand(self, op):
		pass
	def html_operand(self, op):
		pass
	def text_operand(self, op):
		pass
	
	def operand(self, op, format='text'):
		str = ''
		return str

	def xml_data(self, data):
		pass
	def html_data(self, data):
		pass
	def text_data(self, data):
		pass
	
	def data(self, data, format='text'):
		str = ''
		return str


if __name__ == '__main__':
	pass
