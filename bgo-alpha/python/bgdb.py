#!/usr/bin/python
'''
	Big O Database class
'''


# this global should prob be re-coded as a singleton, but
# there is really no need aside from satisfying OOP nazis ;)
__default_db = None

'''
class FakeDatabase(object):
	def type(self):
		return 'Fake'
	def connection(self):
		return self
	def connection_str(self):
		return None
	def connect(self):
		return True
	def create(self):
		return True
	def begin(self):
		pass
	def commit(self):
		pass
	def disconnect(self):
		pass
	def cursor(self):
		return self
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
				  join_columns=None, order_by_col = None):
		return None
	def fetch_all(self, table, where_columns=None, 
				  join_columns=None, order_by_col=None):
		return None
	def blob(self, data):
		pass
	def insert(self, table, columns):
		return 1
	def update(self, table, db_id, columns):
		return True
	def delete(self, table, db_id):
		return True
'''

def default_database():
	global __default_db

	#if __default_db is None:
		# for debugging -- e.g. calling dbobject scripts directly
	#	return FakeDatabase()

	return __default_db

def set_default_database(db):
	global __default_db
	__default_db = db

# General Database Interface
class Database(object):
	def __init__(self, type=str, conn_str=str):
		self._type = type
		self._conn_str = conn_str
		self._conn = None
		self._cur = None
		
		if default_database() is None:
			set_default_database(self)

		# connect to database
		try:
			self.connect()
		except Exception, e:
			print str(e)
			raise e

		# create the database schema
		if not self._detect_schema():
			self.create()

		self._cur = self.cursor()

	def _detect_schema(self):
		if self._conn is None:
			raise AssertionError, 'DB is not connected'

		cu = self._conn.cursor()
		try:
			cu.execute('SELECT count(*) FROM bgo_module')
			row = cu.fetchone()
			cu.close()
		except Exception, e:
		#except OperationalError, e:
			#print 'DB DETECT ERR', str(e)
			#raise(e)
			return False


		if row[0]:
			return True

		return False

	#--------------------------------------------------------
	# BG DB Interface
	# - Member Access
	def type(self):
		return self._type

	def connection(self):
		return self._conn

	def connection_str(self):
		return self._conn_str

	# - Actions
	def connect(self):
		raise AssertionError, "BGDB Virtual connect() called"

	def create(self):
		cu = self.cursor()
		try:
			cu.execute(self._schema_src)
			self._conn.commit()
			cu.close()
		except Exception, e:
			print 'DB CREATE ERR ' + str(e)
			raise e

	def begin(self):
		pass
		#try:
		#	self._cur.execute('BEGIN;')
		#except Exception, e:
		#	print 'DB BEGIN ERR: ' + str(e)
		#	raise e
	
	def commit(self):
		try:
			#self._cur.execute('COMMIT;')
			self._conn.commit()
		except Exception, e:
			print 'DB COMMIT ERR: ' + str(e)
			raise e
	
	def rollback(self):
		try:
			self._conn.rollback()
		except Exception, e:
			print 'DB ROLLBACK ERR: ' + str(e)
			raise e

	def disconnect(self):
		if self._conn is None:
			raise AssertionError, "DB is not connected"

		if self._cur is not None:
			self._cur.close()

		self._conn.close()

	def cursor(self):
		return self._conn.cursor()

	def execute(self, stmt):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		#cur = self.cursor()
		cur = self._cur

		try:
			cur.execute(stmt)
			#cur.close()
		except Exception, e:
			print 'DB EXEC ERR: ' + str(e)
			print stmt
			raise e

	def fetch_id_where(self, table, where_clause, table_alias=None):
		if table_alias is not None:
			id_str = table_alias + '.id'
		else:
			id_str = 'id'

		stmt = 'SELECT ' + id_str + ' FROM ' + table + \
			' WHERE ' + where_clause + ' ORDER BY ' + \
			id_str + ' DESC'
		
		id = None
		#cur = self.cursor()
		cur = self._cur
		try:
			cur.execute(stmt)
			row = cur.fetchone()
			#cur.close()
			if row is not None and len(row) > 0:
				id = row[0]
		except Exception, e:
			print 'FETCH_ID_WHERE ERR: ' + str(e)
			print stmt
			raise e

		return id

	def __build_where_clause(self, cols, join_cols=None):
		where_str = ''
		
		if join_cols is not None:
			for i in join_cols.iterkeys():
				buf = i + ' = ' + join_cols[i]
			
				if where_str == '':
					where_str = buf
				else:
					where_str = where_str + ' AND ' + buf
		
		for i in cols.iterkeys():
			buf = i + ' = ' + cols[i]
			
			if where_str == '':
				where_str = buf
			else:
				where_str = where_str + ' AND ' + buf
		
		return where_str

	def fetch_id(self, table, where_columns):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		
		cols = self._prepare_columns(where_columns)
		where_str = self.__build_where_clause(cols)
		
		return self.fetch_id_where(table, where_str)

	def fetch_row(self, table, columns='*', where_columns=None, 
				  join_columns=None, order_by_col=None):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		
		# TODO: clean order_by_col
		stmt = 'SELECT ' + columns + ' FROM ' + table
		
		if where_columns is not None:
			cols = self._prepare_columns(where_columns)
			where_str = self.__build_where_clause(cols, 
				join_columns)
			stmt = stmt + ' WHERE ' + where_str
		
		if order_by_col is not None:
			stmt = stmt + ' ORDER BY ' + order_by_col 
			
		stmt = stmt + ' LIMIT 1'
		
		try:
			#cur = self.cursor()
			cur = self._cur
			cur.execute(stmt)
			print stmt
			
			if cur.description is None:
				return None
			
			row = cur.fetchone()

			if row is None or len(row) < 1 :
				#cur.close()
				return None

			# create sequence of tuples
			num_cols = len(cur.description)
			# ...create a new empty dict
			cols = {}
			
			# foreach column in row tuple,
			for i in range(num_cols):
				# ... set val for key $COL_NAME to val in tuple
				cols[cur.description[i][0].lower()] = row[i]
			
			#cur.close()
			return cols
		
		except Exception, e:
			print 'FETCHROW ERR ' + str(e)
			print stmt
			raise e

	def fetch_columns(self, table, columns, where_columns=None, 
				  join_columns=None, order_by_col = None):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		
		stmt = 'SELECT ' + columns + ' FROM ' + table
		if where_columns is not None:
			cols = self._prepare_columns(where_columns)
			where_str = self.__build_where_clause(cols, 
				join_columns)
			stmt = stmt + ' WHERE ' + where_str
			
		if order_by_col is not None:
			stmt = stmt + ' ORDER BY ' + order_by_col + ' LIMIT 1'
		
		print stmt
		try:
			#cur = self.cursor()
			cur = self._cur
			cur.execute(stmt)
			rows = []		# return val: array of dicts
			
			if cur.description is None:
				return None
			
			results = cur.fetchall()	# sql query results

			if results is None or len(results) < 1 :
				#cur.close()
				return None

			num_cols = len(cur.description)
			
			# foreach row,
			for r in results:
				# ...create a new empty dict
				cols = {}
				# foreach column in row tuple,
				for i in range(num_cols):
					cols[cur.description[i][0].lower()] = \
						r[i]
				# ...append dict to output array
				rows.append(cols)
			
			#cur.close()
			
		except Exception, e:
			print 'FETCHCOLUMN ERR ' + str(e)
			print stmt
			raise e
		
		return rows
	
	def fetch_all(self, table, where_columns=None, 
				  join_columns=None, order_by_col=None):
		return self.fetch_columns('*', where_columns, join_columns, 
				order_by_col)

	def _prepare_str(self, str):
		# TODO: pwquote
		return "'" + str + "'";
	
	def blob(self, data):
		pass

	def _prepare_bindvars(self, columns):
		bind_vars = []

		for c in columns.iterkeys():
			val = columns[c]
			# for now only BLOB types need bindvars
			if isinstance(val, self.blob_instance()):
				bind_vars.append(val)

		return bind_vars

	def _prepare_columns(self, columns):
		cols = {}

		for c in columns.iterkeys():
			val = columns[c]
			if isinstance(val, int):
				cols[c] = str(val);
			elif isinstance(val, long):
				cols[c] = str(val);
			elif isinstance(val, float):
				cols[c] = str(val);
			elif val is None:
				cols[c] = 'NULL';
			elif isinstance(val, str):
				cols[c] = self._prepare_str(val)
			elif isinstance(val, self.blob_instance()):
				cols[c] = self.bind_var()
			elif isinstance(val, list):
				# make |-delim
				pass
			else:
				raise AssertionError, 'UNK ' + str(type(val)) +\
					' at column ' + c
		return cols

	def insert(self, table, columns):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		cols = self._prepare_columns(columns)
		bind_vars = self._prepare_bindvars(columns)

		# build insert column list
		insert_cols = ""
		for i in cols.iterkeys():
			if insert_cols == "":
				insert_cols = i
			else:
				insert_cols = insert_cols + ', ' + i

		# build insert value list
		insert_vals = ""
		for i in cols.iterkeys():
			if insert_vals == "":
				insert_vals = cols[i]
			else:
				insert_vals = insert_vals + ', ' + cols[i]

		stmt = 'INSERT INTO ' + table + '(' + insert_cols + \
			') VALUES (' + insert_vals + ')'
		#print stmt
		
		#TODO: perform insert, get last_id
		#cu = self._conn.cursor()
		cu = self._cur
		try:
			cu.execute(stmt, bind_vars)
		except Exception, e:
			print "DB ERR " + str(e)
			print stmt
			raise e

		id = 0
		stmt = 'SELECT id FROM ' + table + ' ORDER BY id DESC LIMIT 1'
		#print stmt
		try:
			cu.execute(stmt)
			row = cu.fetchone()
			if row is not None and len(row) > 0:
				id = row[0]
			#self._conn.commit()
		except Exception, e:
			print "DB ERR " + str(e)
			print stmt
			raise e

		#cu.close()
			
		return id 
	
	def update(self, table, db_id, columns):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		cols = self._prepare_columns(columns)

		# build update list
		update_cols = ""
		for i in cols.iterkeys():
			buf = i + '=' + cols[i]
			if update_cols == "":
				update_cols = buf
			else:
				update_cols = update_cols + ', ' + buf

		stmt = 'UPDATE ' + table + ' SET ' + update_cols + \
			' WHERE id = ' + str(db_id)
		#print stmt
		
		#cu = self._conn.cursor()
		cu = self._cur
		try:
			cu.execute(stmt)
			#self._conn.commit()
		except Exception, e:
			print "DB ERR " + str(e)
			raise e

		return 1
	
	def delete(self, table, db_id):
		if self._conn is None:
			raise AssertionError, "DB is not connected"
		print 'DELETE FROM ' + table + 'WHERE id = ' + str(db_id)
		# TODO: perform delete


if __name__ == "__main__":
	db = Database("debug")
	db.connect("project")
	db.disconnect()
