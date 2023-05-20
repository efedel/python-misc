#!/usr/bin/python
'''
	Big O File class factory
'''

import os
import sys
# -- bgo --
import BGFile
import BGObjFile
from file_modules.magic import magic

def FileFactory(path):
	'''
	   Returns a file object representing file a path
	   without fail. Does not stat object. Probably should.
	'''
	if path == None:
		raise ValueError, "Attempt to create file 'None'"

	# determine file type by magic number
	try:
		mgc = magic.Magic("file_modules/magic/magic.linux", 'delete-me')
		ident = mgc.classify(path)
		format = ident.split(' ', 1)[0]
	
		# get MIME type, in case this is an unrecognized object file
		mgc = magic.Magic("file_modules/magic/magic.mime", 'delete-me')
		mime = mgc.classify(path)
	finally:
		# having delete-me lie around because of a Ctrl-C here is BAD!
		try:
			os.unlink('delete-me')
		except OSError, e:
			pass

	
	try :
		module = __import__( 'file_modules.' + format, globals(), 
		                     locals(), (format,) )
		try:
			# Class must be named formatFile !
			f_class = getattr(module, format + "File")
			f = f_class(path, ident)
			return f

		except Exception, e:
			# if any part of this fails, there is something
			# wrong with the parser... return ObjFile
			sys.stderr.write("Error with file module " + \
			                  format + "File : " + str(e) + "\n")
			
			return BGObjFile.ObjFile(path, ident)

	except ImportError, e:
		# Unsupported file format -- no module in binformat/
		if mime.find('executable') != -1:
			# this is object code -- return generic obj file
			return BGObjFile.ObjFile(path, ident)
		else:
			# no idea what this is -- ust a plain file
			return BGFile.File(path, ident)
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: " + sys.argv[0] + " filename\n"
		sys.exit(1)

	f = FileFactory(sys.argv[1])

	print "Format: " + f.format() + " IDENT " + f.ident()
	print "File Object: " + str(f) 
