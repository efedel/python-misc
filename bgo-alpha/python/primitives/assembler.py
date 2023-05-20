#!/usr/bin/python
'''
	Base Assembler virtual class
'''
class AssemblerColors(object):
	def __init__(self, colors):
		''' colors is a dict of type->color mappings:
			immediate/relative operand
			address operand
			 overrides, in order
			 address in code section
			 address in stack [?]
			 address in heap [?]
			 address in data section
			 address in rsrc section
			 address in reloc section
			 address in header section
			register operand
			constant operand
			 overrides, in order
			 operand read
			 operand written
			 operand executed
			 implicit operand
			prefix mnemonic
			mnemonic
			 overrides, in order
			 arithmetic mnemonic
			 bit mnemonic
			 compare mnemonic
			 controlflow mnemonic
			 loadstore mnemonic
			 logic mnemonic
			 misc mnemonic
			 stack mnemonic
			 system mnemonic
			 trap mnemonic
			symbol
			comment
			punctuation
			hex bytes
			read cross reference
			write cross reference
			exec cross reference
			address
			 overrides [in order]
			 address in code section
			 address in data section
			 address in header section
			 address in note section
			 address in resource section
			 address in debug section
			 address in reloc section
			ascii string
			unicode string
			
			...handle with operand, address, insn callbacks.
			i.e. make a callable not a string.
			
			evaluate in order added
		'''
		pass
			
			
		self._colors = colors
class Assembler(object):
	'''
	   Produces string representation of a file,
	   section, instruction, operand, or data
	   object suitable for input to an assembler.
	   
	   Each assembler is expected to support the following
	   formats: text, html, and xml. Additional formats
	   could include rtf, pdf, and doc.
	  
	   The virtual Assembler class just returns the 
	   XML version of each object obtained by calling
	   repr(). 
	'''
	def __init__(self, options=""):
		self._name = 'internal'
		self._options = options

	def file_header(self, file):
		return repr(file)
		
	def file_footer(self, file):
		return repr(file)
	
	def disasm_buffer(self, buf):
		str = ''
		for i in buf.instructions():
			str = str + repr(i)
		
		return buf

	def section_header(self, section):
		return repr(section)
	
	def section_footer(self, section):
		return repr(section)
	
	def function_header(self, func):
		pass
	
	def function_footer(self, func):
		pass

	def instruction(self, insn):
		return repr(insn)
	
	def operand(self, op):
		return repr(op)
	
	def data(self, data):
		return repr(data)

if __name__ == '__main__':
	pass
