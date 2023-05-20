#!/usr/bin/python

import sys
import os.path
sys.path.append(".")
# -- bgo --
import dbobject
import BGProject as project
import BGDisasmFactory as disasmfactory

if __name__ == '__main__':
	db_filename = ''
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + 'file'
		sys.exit(1)
	elif len(sys.argv) == 3:
		db_filename = sys.argv[2]
		
	# this is needed to avoid a huge save at the end
	dbobject.enable_autosave()

	print "BGO STDOUT DB and Disasm Test\n"
	
	name = os.path.basename(sys.argv[1])
	print "Creating project and database..."
	proj = project.Project(name, 'stdout', None )
	print "Processing file..."
	proj.add_file(sys.argv[1])

	for f in proj.files():
		print 'FILE ' + f.name()
		for s in f.sections():
			print 'SECTION ' + s.name() + ' (' + s.access_str() + \
					') : ' + s.flags_str()
			if s.access() & s.ACCESS_X:
				s.disassemble()
				print 'DISASSEMBER: ' + s.arch() 
				for i in s.instructions():
					pass
				print 'Saving disassembly...'
				s.save()

	print "Saving..."

	proj.save()
	print "Done."


