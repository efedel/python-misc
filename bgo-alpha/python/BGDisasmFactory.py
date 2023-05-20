#!/usr/bin/python

import os
import sys
# -- bgo --

def DisasmFactory(cpu, options=None):
	'''
	   Returns a disassembler object based on CPU type.
	   'options' is disassembler-specific.
	'''
	if cpu == None:
		raise ValueError, "Attempt to load disassembler 'None'"
	
	try :
		module = __import__( 'disasm_modules.' + cpu, globals(), 
		                     locals(), (cpu,) )
		try:
			# Class must be named cpuDisasm !
			d_class = getattr(module, cpu + "Disasm")
			d = d_class(options)
			return d

		except Exception, e:
			sys.stderr.write("Error with cpu module " + \
			                  cpu + " : " + str(e) + "\n")
			raise e

	except ImportError, e:
		sys.stderr.write("No such cpu module " + \
						cpu + " : " + str(e) + "\n")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " cpu\n"
		sys.exit(1)

	d = DisasmFactory(sys.argv[1])

	print "Disassembler Object: " + str(d) 
