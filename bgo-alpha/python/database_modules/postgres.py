#!/usr/bin/python
'''
	Big O Postgres Database module
'''

import array
from pyPgSQL import PgSQL

# --bgo--
import bgdb
import database_modules.schema.bg_pgsql as bg_pgsql


class postgresDatabase(bgdb.Database):
	#import InterfaceError, DatabaseError, DataError, OperationalError, \
	#	IntegrityError, InternalError, ProgrammingError from pyPgSQL
	
	def __init__(self, conn_str):
		self._conn = None

		self._schema_src = bg_pgsql.bgo_schema_str()

		bgdb.Database.__init__(self, 'postgres', conn_str)

	def connect(self):
		try:

			self._conn = PgSQL.connect(self._conn_str)
		except Exception, e:
			print 'DB CONN ERR ' + str(e)
			raise e

	def bind_var(self):
		return '%s'

	def blob_instance(self):
		return PgSQL.PgBytea

	def blob(self, data):
		if isinstance(data, str):
			return PgSQL.PgBytea(data)
		return None



if __name__ == "__main__":
	db = Database("postgres")
	db.connect("")
	db.disconnect()
