#!/usr/bin/python

import sys
import os.path
sys.path.append(".")
# -- bgo --
import dbobject
import BGProject as project
import BGDisasmFactory as disasmfactory

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + 'file'
		sys.exit(1)

	dbobject.enable_autosave()

	print "BGO Postgres DB and Disasm Test\n"
	
	name = os.path.basename(sys.argv[1])
	print "Creating project and connecting to database..."
	# remember to do 'CREATE USER username;' in `psql phdb` !
	proj = project.Project(name, 'postgres', 'localhost::bgo::' )

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
					#print repr(i)
					pass
	
	print "Saving..."
	proj.save()
	print "Done."


