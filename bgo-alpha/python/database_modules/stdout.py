#!/usr/bin/python
'''
	Big O STDOUT Database module
	prints DB statements to STDOUT
'''

import array
import os

# --bgo--
import bgdb


class stdoutDatabase(bgdb.Database):

	# import SQLite exceptions into DB object
	#from pysqlite2 import InterfaceError, DatabaseError, \
	#	DataError, OperationalError, IntegrityError, InternalError, \
	#	ProgrammingError, NotSupportedError

	def __init__(self, conn_str):
		self.__counter  = 0

		# initialize DB object
		# this will invoke self.connect() and, if needed, self.create()
		bgdb.Database.__init__(self, 'stdout', conn_str)

	def connect(self):
		self._conn = 1
		return True

	def _detect_schema(self):
		return True
	
	def create(self):
		pass
	
	def begin(self):
		pass

	def close(self):
		pass
	
	def commit(self):
		pass
	
	def bind_var(self):
		return '?'

	def blob_instance(self):
		return None

	def blob(self, data):
		if isinstance(data, str):
			return buffer(data)
		return None

	def cursor(self):
		return self

	def execute(self, stmt):
		return True

	def fetch_id_where(self, table, where_clause, table_alias=None):
		if table_alias is not None:
			id_str = table_alias + '.id'
		else:
			id_str = 'id'

		stmt = 'SELECT ' + id_str + ' FROM ' + table + \
			' WHERE ' + where_clause + ' ORDER BY ' + \
			id_str + ' DESC'
		
		print stmt

		return None

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

	def fetchone(self):
		return None

	def fetch_id(self, table, where_columns):
		cols = self._prepare_columns(where_columns)
		where_str = self.__build_where_clause(cols)
		
		return self.fetch_id_where(table, where_str)

	def fetch_row(self, table, columns='*', where_columns=None, 
				  join_columns=None, order_by_col=None):
		
		# TODO: clean order_by_col
		stmt = 'SELECT ' + columns + ' FROM ' + table
		
		if where_columns is not None:
			cols = self._prepare_columns(where_columns)
			where_str = self.__build_where_clause(cols, join_columns)
			stmt = stmt + ' WHERE ' + where_str
		
		if order_by_col is not None:
			stmt = stmt + ' ORDER BY ' + order_by_col 
			
		stmt = stmt + ' LIMIT 1'

		print stmt

		return None
		

	def fetch_columns(self, table, columns, where_columns=None, 
					  join_columns=None, order_by_col = None):
		stmt = 'SELECT ' + columns + ' FROM ' + table
		if where_columns is not None:
			cols = self._prepare_columns(where_columns)
			where_str = self.__build_where_clause(cols, join_columns)
			stmt = stmt + ' WHERE ' + where_str
			
		if order_by_col is not None:
			stmt = stmt + ' ORDER BY ' + order_by_col + ' LIMIT 1'
		
		print stmt
		return None
	
	def fetch_all(self, table, where_columns=None, 
				  join_columns=None, order_by_col=None):
		return self.fetch_columns('*', where_columns, join_columns, 
				order_by_col)

	def _prepare_str(self, str):
		# TODO: pwquote
		return "'" + str + "'";
	
	def blob_instance(self):
		return buffer

	def blob(self, data):
		if isinstance(data, str):
			return buffer(data)
		return None

	def _prepare_bindvars(self, columns):
		bind_vars = []

		for c in columns.iterkeys():
			val = columns[c]
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

		print stmt
		self.__counter += 1
		print '-- INSERT resulted in ID ' + str(self.__counter)

		# return fake id
		return self.__counter
	
	def update(self, table, db_id, columns):
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
		print stmt

		return True
		
	
	def delete(self, table, db_id):
		return True


if __name__ == "__main__":
	db = Database("stdout")
	db.connect(None)
	db.disconnect()
