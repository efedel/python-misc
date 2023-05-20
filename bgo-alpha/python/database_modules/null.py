#!/usr/bin/python
'''
	Big O /dev/null Database module
'''

# --bgo--
import bgdb


class nullDatabase(bgdb.Database):

	# import SQLite exceptions into DB object
	#from pysqlite2 import InterfaceError, DatabaseError, \
	#	DataError, OperationalError, IntegrityError, InternalError, \
	#	ProgrammingError, NotSupportedError

	def __init__(self, conn_str):
		bgdb.Database.__init__(self, conn_str)

	def connect(self):
		# database connection
		self._conn = 1
		return True

	def disconnect(self):
		return True

	def _detect_schema(self):
		return True

	def create(self):
		pass
	
	def begin(self):
		pass
	
	def commit(self):
		pass
	
	def bind_var(self):
		return '?'

	def blob_instance(self):
		pass

	def cursor(self):
		return self
	
	def fetchone(self):
		return None
	
	def close(self):
		pass

	def execute(self, stmt):
		return True

	def fetch_id_where(self, table, where_clause, table_alias=None):
		return None

	def fetch_id(self, table, where_columns):
		return None

	def fetch_row(self, table, columns='*', where_columns=None,
			join_columns=None, order_by_col=None):
		return None

	def fetch_columns(self, table, columns, where_columns=None,
			join_columns=None, order_by_col=None):
		return None

	def fetch_all(self, table, where_columns=None,
			join_columns=None, order_by_col=None):
		return None

	def blob(self, data):
		if isinstance(data, str):
			return buffer(data)
		return None

	def insert(self, table, columns):
		return 1
	
	def update(self, table, db_id, columns):
		return True

	def delete(self, table, db_id):
		return True

if __name__ == "__main__":
	db = Database("null")
	db.connect(None)
	db.disconnect()
