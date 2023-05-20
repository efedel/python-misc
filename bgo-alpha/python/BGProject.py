#!/usr/bin/python
'''
	Big O Project class
'''

import sys
# -- bgo --
import bgdb
import BGDBFactory
import BGFileFactory
import dbobject
import primitives.project as project

DEFAULT_DB_LOC = '~/.bgo/'

class Project(project.Project, dbobject.DBObject):
	def __init__(self, name=None, db_type=None, conn_str=None, \
			force_clean=False):
		# project makes the DB connect() for all DBObjects
		db = self.__get_db(db_type, conn_str)
		
		if db == None:
			raise AssertionError, 'No database present'
		
		# set version to default value
		self._version = 1.0
		
		# check if project already exists in database
		db_id = db.fetch_id('project', {'name' : name})
		if db_id is not None and force_clean:
			# exists; increment version and do not restore
			# this will cause a new row to be inserted
			cols = db.fetch_columns( 'project', 'version', {'id' : db_id})
			version = cols[0]['version']
			if version is None:
				version = 1.0
			self._version = version + 1.0
			db_id = None
		
		# DBObject init will restore if db_id is not None
		dbobject.DBObject.__init__(self, db, id=db_id)
		if db_id is not None:
			# we restored, no need to continue init
			return
		
		project.Project.__init__(self, name)


	# BG Project Interface overrides
	def add_file(self, path, force_clean=False):
		if path in self.files():
			# TODO : raise warning exception
			pass
		
		if not force_clean:
			pass
		# if file exists in DB with same md5sum, use it
		# if [ ... ] f.db_id = ;
		# else :
		f = BGFileFactory.FileFactory(path)
		self._files.append(f)
		self.autosave()

	def remove_file(self, path):
		project.Project.removeS_file(self, path)
		
		self.autosave()
	
	def __get_db(self, db_type, conn_str):

		if db_type is None:
			# no db type; maybe user is trying for the default db
			db = bgdb.default_database()
			if db :
				return db
			else:
				db_type = 'sqlite3'

		if conn_str == None and db_type == 'sqlite3':
			conn_str = DEFAULT_DB_LOC + self.name() + '.bgo'
		
		# create and connect to Database
		db = BGDBFactory.DatabaseFactory(db_type, conn_str)

		return db

	# DBObject Interface
	def __save(self):
		if not self.db_id():
			self._db_id = self.db().insert('project', 
				{ 'name' : self.name(),
				  'version' : self._version	})

		# TODO real insert
		self._db_id = 1
		#else :
		#	self.db().update('project', self.db_id() 
		#		{ 'name' : self._name(),
		#		 'mod_date' : 
		#		 self.db().dbi().TimestampFromTicks(time.localtime(ticks)[:6])
		self._dirty = 0
	
	def save(self):
		if self._dirty:
			self.__save()
		
		for f in self._files:
			# save file to db
			f.save()
			
			id = self.db().fetch_id('project_file_map',
				{ 'project' : self.db_id(),
				  'file' : f.db_id() } )
			
			if not id:
				# add row to map table
				self.db().insert( 'project_file_map',
					{ 'project' : self.db_id(),
					  'file' : f.db_id() } )

	def restore(self):
		print "Restoring project..."
		# select details from project
		
		rows = self.db().fetch_columns( 'project', 'version', 
				{ 'id' : self.db_id() } )
		
		if rows[0]['version'] is not None:
			self._version = rows[0]['version']
		
		self._files = [] 
		
		# foreach file in project_file_map
		# get id of file and of module_class for file from DB
		rows = self.db().fetch_columns( 
				'project_file_map, file',
				'project_file_map.file, file.class', 
				{ 'project_file_map.project' : self.db_id() },
				{ 'project_file_map.file' : 'file.id' } )
		
		for row in rows:
			id = row['file']
			mod_cls_id = row['class']
			file = dbobject.BuildModuleClass(self.db(), mod_cls_id, id)
			self._files.append( file )
		# foreach process_image in project_process_map
		#	process(db_id)
		# foreach symbol in project_symbol_map
		#	symbol(db_id)
		# foreach comment in project_comment_map:
		#	comment(db_id)

	def delete(self):
		
		dbobject.DBObject.delete(self)
		
		for f in self._files:
			# remove from mapping table
			# if no more mappings, remove from db
			pass
	


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Usage: " + sys.argv[0] + \
			" name db_type conn_str [files]\n"
		sys.exit(1)

	p = Project(sys.argv[1], sys.argv[2], sys.argv[3])

	print "Project " + sys.argv[1] + " created."
	
	for i in range( 4, len(sys.argv) ):
		print "Adding file " + sys.argv[i]
		p.add_file( sys.argv[i] )

	p.export('/tmp/' + p.name() + '.bgo')
