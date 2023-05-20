#!/usr/bin/python

import sys
import os.path
#import threading
sys.path.append(".")
# -- bgo --
import dbobject
import BGProject as project
import BGDisasmFactory as disasmfactory

#class BackgroundSave(threading.Thread):
#	def __init__(self, section):
#		threading.Thread.__init__(self)
#		self._section = section
#	def run(self):
#		self._section.save()

if __name__ == '__main__':
	db_filename = ''
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + 'file'
		sys.exit(1)
	elif len(sys.argv) == 3:
		db_filename = sys.argv[2]
		
	# this is needed to avoid a huge save at the end
	dbobject.enable_autosave()

	print "BGO SQLite3 DB and Disasm Test\n"
	
	name = os.path.basename(sys.argv[1])
	if db_filename == '':
		db_filename = '/tmp/' + name + '.bgo'
	print "Creating project and database..."
	proj = project.Project(name, 'sqlite3', db_filename )
	print "Processing file..."
	proj.add_file(sys.argv[1])

	#threads = []

	for f in proj.files():
		print 'FILE ' + f.name()
		for s in f.sections():
			s.db().begin()
			print 'SECTION ' + s.name() + ' (' + s.access_str() + \
					') : ' + s.flags_str()
			if s.access() & s.ACCESS_X:
				s.disassemble()
				print 'DISASSEMBER: ' + s.arch() 
				#for i in s.instructions():
				#	pass
				print 'Saving disassembly...'
			s.save()
			# start saving sections in background
			#bgsave = BackgroundSave(s)
			#bgsave.start()
			#threads.append(bgsave)
			s.db().commit()

	print "Saving..."
	#for t in threads:
	#	t.join()

	proj.save()
	print "Done."


