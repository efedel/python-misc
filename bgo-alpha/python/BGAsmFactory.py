#!/usr/bin/python
'''
	Big O Assembler class factory
'''

import os
import sys
# -- bgo --

def AsmFactory(asm, options=None):
	'''
	   Returns an assembler object based on asm format.
	   'options' is assembler-specific.
	'''
	if asm == None:
		raise ValueError, "Attempt to load assembler 'None'"
	
	try :
		module = __import__( 'assembler_modules.' + asm, globals(), 
		                     locals(), (asm,) )
		try:
			# Class must be named asmDisasm !
			d_class = getattr(module, asm + "Assembler")
			d = d_class(options)
			return d

		except Exception, e:
			sys.stderr.write("Error with asm module " + \
			                  asm + " : " + str(e) + "\n")
			raise e

	except ImportError, e:
		sys.stderr.write("No such asm module " + \
						asm + " : " + str(e) + "\n")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " asm\n"
		sys.exit(1)

	a = AsmFactory(sys.argv[1])

	print "Assembler Object: " + str(a) 
