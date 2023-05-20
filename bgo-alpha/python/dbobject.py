#!/usr/bin/python
'''
	Big O Persistent (Database) Object class
'''

import thread
# --bgo--
import bgdb

# autosave flag: shared by all DB Objects
__autosave = 0

def handle_obj_type(obj, name, type):
	if (type == 'NoneType'):
		pass
	elif type == 'list' or type == 'dict':
		# pickle
		pass
	elif type == 'Set':
		# foreach set
		pass
	elif type == 'str':
		pass
	elif type == 'int':
		pass
	else:
		# treat as object -- save
		pass
	
def save(object):
	for i in object.__dict__.iterkeys:
		otype = type(object.__dict__[i]).__name__
		handle_otype()

def enable_autosave():
	global __autosave
	__autosave = 1

def disable_autosave():
	global __autosave
	__autosave = 0

def autosave_enabled():
	global __autosave
	return __autosave

class DBObject(object):
	''' 
	   DB Object: An object backed by the database store
	'''

	def __init__(self, db=None, id=None):
		'''
		   Must be invoked by all subclasses
		'''
		# name of DB table that stores this object
		self._db_table = None
		
		# get database object
		if db is None:
			self._db = bgdb.default_database()
		else:
			self._db = db
		
		# all objects are clean initially
		self._dirty = 0

		# TODO: remove this?
		self._lock = thread.allocate_lock()

		self._db_id = id

		if self._db_id is not None:
			# if a DBObject constructor specifies a DB id,
			# restore the object from the db. This may be the
			# best we can do with python's lame approach to
			# polymorphism...
			self.restore()

#	def __db_values(self):
#		''' 
#		   return a hash of all object members to be saved in db
#		   NOTE: this MUST be overridden by subclasses, and
#		             the db_id key must be set to self._db_id
#		'''
#		return { 'db_id' : self._db_id }

	def save(self):
		'''
		   save object to database. subclasses can inherit this,
		   or override it to save 'children' and then invoke
		   it to save themselves
		'''
		return 1
		
		dirty = 0

		if self._lock.acquire() :
			dirty = self._dirty
			self._lock.release()
		else:
			# we should probably throw an exception here
			# but that would break things if no one catches
			# it. bette just to return failure.
			return False

		if dirty == 0:
			# nothing to do: return 'saved'
			return True

		# get table name and object values to pass to DB
		table = self._db_table
		values = None
		if self._lock.acquire() :
			values = self.__db_values()
			self._lock.release()
		else:
			# once again, we return false due to lock issues
			return False

		db = bgdb.default_database()
		if db == None:
			# No database: return failure
			return False

		# OK, finally write to the DB
		if db.save_object( table, values ):
			if new_row:
				self._db_id = values['db_id']
		
		if self._lock.acquire() :
			self._dirty = 0
			self._lock.release() 
			# no else; we don't care if this one fails
		
		return True

	def delete(self):
		'''
		   delete from database. subclasses can inherit this,
		   or override it to delete 'children' and then invoke
		   it to delete themselves
		'''
		return 1
		# get table name and object values to pass to DB
		table = self._db_table
		values = None
		if self._lock.acquire() :
			values = self.__db_values()
			self._lock.release()
		else:
			# once again, we return false due to lock issues
			return False

		db = bgdb.default_database()
		if db == None:
			# No database: return failure
			return False
		
		# remove from the DB
		return db.delete_object( table, values['db_id'] )

	def restore(self, db_id, values=None):
		pass

	def autosave(self):
		'''
		   autosave hook. call this at the end of each
		   method that modifies the object. Note that
		   this marks the object as dirty even if
		   autosave is disabled!
		'''
		
		self._dirty = 1
		if autosave_enabled() != 0 :
			self.save()
	
	def db(self):
		if self._db is None:
			return bgdb.default_database()
		return self._db
	
	def db_id(self):
		return self._db_id

	def dirty(self):
		''' 
		    Mark the DBObject as dirty. This is used when the
		    object has been modified but has not been saved --
		    for example, on construction of a BGInstruction 
		    that has not had its members set by the disassembler.
		'''
		self._dirty = 1

def BuildModuleClass( db, db_id, obj_db_id ):
	'''
		a general-purpose object factory that restores a
		module-specific class instance, e.g. a File or
		Instruction subclass.
	'''	
	row = db.fetch_row( 'module_class', 
			'filename, classname',	{ 'id' : db_id } )
	mod_name = row['filename']
	class_name = row['classname']
	print "Creating class " + class_name + " from module " + mod_name
	
	try :
		instance = None
		module = __import__( mod_name, globals(), 
		                     locals(), (mod_name,) )
		# Class must be named formatFile !
		class_def = getattr(module, class_name)
		instance = class_def(db_id=obj_db_id)

	except ImportError, e:
		# log unavailable module
		print 'Error with module: ' + mod_name
		print str(e)
		# raise e
	
	return instance
