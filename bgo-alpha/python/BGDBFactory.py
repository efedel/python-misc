#!/usr/bin/python
'''
	Big O Database class factory
'''

import sys

def DatabaseFactory(type, connect_str):
	try :
		module = __import__( 'database_modules.' + type, globals(), 
		                     locals(), (type,) )
		try:
			# Class must be named formatFile !
			f_class = getattr(module, type + "Database")
			f = f_class(connect_str)
			return f

		except Exception, e:
			sys.stderr.write("Error with BGDB module " + \
			                 type + "Database : " + str(e) + "\n")
			raise e

	except ImportError, e:
		sys.stderr.write("Error with BGDB module " + \
		                  type + "Database : " + str(e) + "\n")
		raise e

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: " + sys.argv[0] + " db_type conn_str\n"
		sys.exit(1)

	db = DatabaseFactory(sys.argv[1], sys.argv[2])

	print "Connecting DB " + str(db) + "\n"
	db.connect()
	db.disconnect()
	print "DB " + str(db) + "disconnected\n"
