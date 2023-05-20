#!/usr/bin/python

import sys
import os.path
import profile
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

def main():
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + 'file'
		sys.exit(1)

	# this is needed to avoid a huge save at the end
	dbobject.enable_autosave()

	print "BGO SQLite3 DB and Disasm Test\n"
	
	name = os.path.basename(sys.argv[1])
	print "Creating project and database..."
	proj = project.Project(name, 'sqlite3', '/tmp/' + name + '.bgo' )
	print "Processing file..."
	proj.add_file(sys.argv[1])

	#threads = []

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
			# start saving sections in background
			#bgsave = BackgroundSave(s)
			#bgsave.start()
			#threads.append(bgsave)

	print "Saving..."
	#for t in threads:
	#	t.join()

	proj.save()
	print "Done."

if __name__ == '__main__':
	profile.run('main()')

