#!/usr/bin/python

# this global should prob be re-coded as a singleton, but
# there is really no need aside from satisfying OOP nazis ;)
default_db = None

def default_database():
	return default_db

# General Database Interface
class Database:
	def __init__(self, type=str, path=str):
		self.__type__ = type
		self.__conn__ = None

		# set path to schema sql source
		if path is not None:
			# TODO: change this to /usr/share/bgo
			#       or ~/.bgo
			path = "./"

		self.__schema_src__ = path + "bgo_schema.sql"

		if default_db is None:
			default_db = self

	def connect(self, args):

		# SQLite
		if self.__type__ == "sqlite":
			import sqlite
			self.__conn__ = sqlite.connect(args + ".bgo")
			cu = self.__conn__.cursor()
			cu.execute("""
				SELECT count(*) FROM sqlite_master
				WHERE type='table'
				""")
			row = cu.fetchone()
			if not row[0]:
				self.create()

			return True

		# Postgres
		elif self.__type__ == "postgres":
			from pyPgSQL import PgSQL
			self.__conn__ = PgSQL.connect(args)
			cu = self.__conn__.cursor()
			cu.execute( """
				SELECT count(*) 
				""")
			row = cu.fetchone()
			if not row[0]:
				self.create()

			return True

		raise AssertionError, "Unsupported database type"

	def disconnect(self):
		if self.__conn__ is None:
			raise AssertionError, "DB is not connected"

		self.__conn__.close()
		self.__conn__ = None

	def execute(self, arg):
		if self.__conn__ is None:
			raise AssertionError, "DB is not connected"

		return self._conn__.execute(arg)

	def fetch_row(self):
		if self.__conn__ is None:
			raise AssertionError, "DB is not connected"

		return self._conn__.fetchone()

	def fetch_all(self):
		if self.__conn__ is None:
			raise AssertionError, "DB is not connected"

		return self._conn__.fetchall()

	def create(self):
		# create all the tables
		f = open(self.__schema_src__)
		schema_src = ""
		lines = f.readlines()
		for i in lines:
			schema_src += i
		f.close()

		cu = self.__conn__.cursor()
		cu.execute(schema_src)
		self.__conn__.commit()



if __name__ == "__main__":
	db = Database("sqlite")
	db.connect("project")
	db.disconnect()
