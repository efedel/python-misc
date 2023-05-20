#!/usr/bin/python
'''
	Base Project class
'''

import sys
# -- bgo --
import file


def Load(filename):
	'''
	   load project from saved XML file
	'''
	pass

class Project(object):
	def __init__(self, name):
		self._name = name
		self._files = []        
		
	def export(self, path):
		'''
		   Write an XML file containing the project.
		   Call self.__str__, which does the same for each
		   file in project
		'''
		buf = self.__str__()
		# open file
		# write buf
	
	def name(self):
		return self._name
	
	def files(self):
		return self._files
	
	def add_file(self, path):
		try:
			# filefactory has been removed from primitive
			# since it relies on BG* classes
			f = file.File(path)
			self._files.append(f)
		except ValueError, e:
			pass
		except IOError, e:
			sys.stderr.write(str(e))
	
	def remove_file(self, path):
		'''
		   Remove file and all sections, insn, etc
		'''
		pass

	def __str__(self):
		# gen XML start
		buf = ""
		
		for f in self._files :
			# gen XML per file
			buf += f.__str__()
		
		# gen XML end
		buf += ""
		
		return buf


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " name [files]\n"
		sys.exit(1)

	p = Project(sys.argv[1])

	print "Project " + sys.argv[1] + " created."
	
	for i in range( 2, len(sys.argv) ):
		print "Adding file " + sys.argv[i]
		p.add_file( sys.argv[i] )

	p.export('/tmp/' + p.name() + '.bgo')
