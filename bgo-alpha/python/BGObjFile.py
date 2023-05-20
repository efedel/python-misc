#!/usr/bin/python
'''
	Big O Object File class
'''

# -- bgo --
import BGFile
import utils.set as set

class ObjFile(BGFile.File):
	_class_db_id = None
	
	def __init__(self, path=None, ident=None, db_id=None):
		
		if self._class_db_id is None:
			# ObjFile is always the second id in the database
			self._class_db_id = self.OBJFILE_DB_ID
		
		BGFile.File.__init__(self, path, ident, db_id)
		if db_id is not None:
			# file has been restored from database
			return
		
		self._type = self.TYPE_EXEC
		self._code = set.Set( get_key = lambda c: c._address )
		
		try:
			self.load()
			self.parse()
			self.autosave()
		except ValueError, e:
			# log
			raise e
		except IOError, e:
			# log
			raise e

	def parse(self):
		# create one large section with the entire
		# file in it, mark as code.
		# set entry point to start of file: treat as
		# binary or ROM image.
		pass
