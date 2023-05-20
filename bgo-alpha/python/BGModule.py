#!/usr/bin/python
'''
	Big O Module/Plugin class
'''

import dbobject

class Module(dbobject.DBObject):

	def __init__(self, name, version=0.1, author='Anonymous', 
	             license='None'):
		self._name = name
		self._version = version
		self._author = author
		self._license = license

		dbobject.DBObject.__init__(self)

		self._db_init()
	
	def _db_init(self):
		id = None
		version = None
		
		# select id, version from db
		result = self.db().fetch_columns( 'bgo_module', 'id, version',
			{ 'name' : self._name } );

		if result is not None:
			row = result[0]
			id = row['id']
			version = row['version']
		
		if id is None or version is None:
			self.db().begin()
			# register module with database
			self.register()
			# insert all required rows
			self.new_install()
			self.db().commit()
			return
		
		if version < self._version:
			# update module registration in db
			self._db().update( 'bgo_module', id,
				{ 'version' : self._version,
				  'author' : self._author,
				  'license' : self._license } )
		self._db_id = id
		self.db().begin()
		# Upgrade gets all row IDs as a side effect
		self.upgrade_install(version)
		self.db().commit()

	def register(self):
		id = self.db().insert( 'bgo_module',
			{ 'name' : self._name, 'version' : self._version,
			  'author' : self._author, 
			  'license' : self._license } )
		self._db_id = id

	def new_install(self):
		''' 
			Insert all module definitions into the database 
		'''
		raise NotImplemented, 'Virtual method called'
	
	def upgrade_install(self):
		''' 
			Update all existing module definitions to 
			be associated with this version. This should
			do a select-or-insert, so tht even if nop rows
			need to be inserted, the ids for all rows are
			retrieved
		'''
		raise NotImplemented, 'Virtual method called'

	def save(self):
		pass

	def autosave(self):
		pass

	def delete(self):
		pass

	def restore(self):
		pass
