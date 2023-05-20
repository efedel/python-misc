#!/usr/bin/python
'''
	Big O SQLite3 Database module
'''

import array
import os
from pysqlite2 import dbapi2 as sqlite

# --bgo--
import bgdb
# schema file
import database_modules.schema.bg_sqlite3 as bg_sqlite3


class sqlite3Database(bgdb.Database):

	# import SQLite exceptions into DB object
	#from pysqlite2 import InterfaceError, DatabaseError, \
	#	DataError, OperationalError, IntegrityError, InternalError, \
	#	ProgrammingError, NotSupportedError

	def __init__(self, conn_str):
		# database connection
		self._conn = None

		# load source for BG DB schema
		self._schema_src = bg_sqlite3.bgo_schema_str()

		# initialize DB object
		# this will invoke self.connect() and, if needed, self.create()
		bgdb.Database.__init__(self, 'sqlite3', conn_str)

	def connect(self):
		
		try:
			self._conn = sqlite.connect(self._conn_str)
			cur = self.cursor()
			#cur.execute('PRAGMA cache_size = 10000;')
			#cur.execute('PRAGMA synchronous = OFF;')
			#cur.execute('PRAGMA count_changes = OFF;')
			#cur.execute('PRAGMA synchronous = NORMAL;')
			cur.execute('PRAGMA synchronous=OFF;')
			cur.execute('PRAGMA count_changes=OFF;')
			cur.execute('PRAGMA temp_store=MEMORY;')
			cur.close()
			self._conn.isolation_level = "IMMEDIATE"
		except Exception, e:
			print 'DB CONN ERR ' + str(e)
			raise e
		return True

	def create(self):
		cur = self.cursor()
		for cmd in self._schema_src.split(';'):
			try:
				cur.execute(cmd)
			except Exception, e:
				print str(e)
		cur.close()
		
		return

	def cursor(self):
		cur = self._conn.cursor()
		#cur.execute('PRAGMA synchronous=OFF')
		#cur.execute('PRAGMA count_changes=OFF')
		#cur.execute('PRAGMA temp_store=2')
		#cur.execute('PRAGMA cache_size=5000')
		return cur
	
	def begin(self):
		#cur = self._conn.cursor()
		#cur.execute('BEGIN TRANSACTION;')
		self._conn.isolation_level = "IMMEDIATE"
		#self._conn.isolation_level = None
	#	try:
	#		cur = self._cur
	#		cur.execute('BEGIN TRANSACTION;')
	#	except Exception, e:
	#		print 'DB BEGIN ERR: ' + str(e)
	#		raise e
	
	#def commit(self):
	#	try:
	#		cur = self._cur
	#		cur.execute('COMMIT TRANSACTION;')
	#	except Exception, e:
	#		print 'DB COMMIT ERR: ' + str(e)
	#		raise e
		
		#self._conn.isolation_level = ''
	
	def bind_var(self):
		return '?'

	def blob_instance(self):
		return buffer

	def blob(self, data):
		if isinstance(data, str):
			return buffer(data)
		return None

if __name__ == "__main__":
	db = Database("sqlite")
	db.connect("project")
	db.disconnect()
