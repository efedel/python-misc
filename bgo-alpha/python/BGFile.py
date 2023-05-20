#!/usr/bin/python
'''
	Big O File class
'''

import sys 
# -- bgo --
import primitives.file as file
import dbobject

class File(file.File, dbobject.DBObject):
	# these will be overridden by child classes
	_class_db_id = None
	_format = None
	
	FILE_DB_ID = 54		# from bgo_schema.sql
	OBJFILE_DB_ID = 55
	
	def __init__(self, path=None, ident=None, db_id=None):
		# initialize database representation
		dbobject.DBObject.__init__(self, id=db_id)
		if db_id is not None:
			return
		
		file.File.__init__(self, path, ident)
		
		if self._format is None:
			self._format = self.FORMAT_UNK
		
		if self._class_db_id is None:
			# File is always the first id in the database
			self._class_db_id = FILE_DB_ID
		
		#self.autosave()

	# File API Overrides
	def add_section(self, section):
		print 'ADD SECT'
		file.File.add_section(self, section)
		print 'SAVE'
		self.autosave()

	def add_insn(self, insn):
		file.File.add_insn(self, insn)

		self.autosave()

	def add_data(self, data):
		file.File.add_data(self, data)

		self.autosave()

	def add_symbol(self, sym):
		file.File.add_symbol(self, sym)

		self.autosave()

	def add_string(self, str):
		file.File.add_string(self, str)

		self.autosave()

	def add_entry(self, addr):
		file.File.add_entry(self, addr)

		self.autosave()

	def add_layer(self, name, ):
		file.File.add_layer(self, name)

		self.autosave()

	# TODO: FIX layer handling
	def __save_layer(self, layer, parent_id):
		# insert layer for code
		id = self.db().insert('layer', 
			{ 'name' : layer['name'], 
			  'parent' : parent_id } )
		# associate layer with file
		self.db().insert('file_layer_map',
			{ 'file' : self.db_id(),
			  'layer' : id } )

		layer['db_id'] = id

	# DBObject Interface
	def __save(self):
		if self._container:
			container = self._container.db_id()
		else:
			container = None
		
		if not self.db_id():
			#create file image object
			image_id = self.db().insert('file_image',
				{ 'host' : 'localhost', #FIXME!
				  'name' : self.path() + '/' + self.name(),
				  'md5sum' : self.md5(),
				  'image' : self.db().blob(self.read()) } )
				
			
			# create file object
			self._db_id = self.db().insert( 'file',
				{ 'name' : self.name(),
				  'path' : self.path(),
				  'type' : self._type[1],
				  'format' : self._format[1],
				  'os' : self._os[1],
				  'arch' : self._arch[1],
				  'class' : self._class_db_id,
				  'container' : container,
				  'image' : image_id,
				  'size' : self.size() } )
		else:
			# update relevant fields in existing object
			self.db().update( 'file', self.db_id(),
				{ 'path' : self.path(),
				  'type' : self._type[1],
				  'format' : self._format[1],
				  'os' : self._os[1],
				  'arch' : self._arch[1],
				  'container' : container } )
		
		self._dirty = 0

	def save(self):
		if self._dirty:
			self.__save()

		layer_parent = None
		for layer in self._layers:
			if not layer['db_id']:
				self.__save_layer(layer, layer_parent)
			layer_parent = layer['db_id']
		
		layer = self._layers[-1]

		for s in self._sections:
			s.save()
		
		for i in self._insn:
			old_id = i.db_id()
			i.save()
			if not old_id:
				# add to mapping table
				self.db().insert('layer_insn_map',
					{ 'layer' : layer['db_id'],
					  'insn' : i.db_id() } )
		
		for d in self._data:
			old_id = d.db_id()
			d.save()
			if not old_id:
				# add to mapping table
				self.db().insert('layer_data_map',
					{ 'layer' : layer['db_id'],
					  'data' : d.db_id() } )
		
		for s in self._symbols:
			old_id = s.db_id()
			s.save()
			if not old_id:
				# add to mapping table
				self.db().insert('file_symbol_map',
					{ 'file' : self.db_id(),
					  'symbol' : s.db_id() } )

		for s in self._strings:
			s.save()

	def delete(self):
		dbobject.DBObject.delete(self)
		
		for s in self._sections:
			s.delete()
		
		for d in data:
			d.delete()
		
		for s in symbols:
			s.delete()
		
		for s in strings:
			s.delete()
	

	def restore(self):
		'''
			Restore File object from DB
		'''
		# select details from file and file_image
		file = self.db().fetch_row( 'file', '*', {'id':self.db_id()} )
		if file is None:
			raise AssertionError, 'Unable to fetch file ' + str(self.db_id())
		self._name = file['name']
		self._path = file['path']
		self._size = file['size']
		self._ident = file['ident']
		
		type = self.db().fetch_row( 'file_type', '*', {'id':file['type']} )
		format =self.db().fetch_row('file_format', '*', {'id':file['format']})
		os = self.db().fetch_row( 'file_os', '*', {'id':file['os']} )
		arch = self.db().fetch_row( 'arch', '*', {'id':file['arch']} )
		
		self._type = (type['name'], type['id'])
		self._arch = (arch['name'], arch['id'])
		self._os = (os['name'], os['id'])
		self._arch = (arch['name'], arch['id'])
		
		image = self.db().fetch_row('file_image', '*', {'id':file['image']} )
		self._md5 = image['md5sum']
		
		# TODO: container
		# TODO: file_image: self._image
			
		# foreach in file_layer_map:
		#	layer(id)
		# foreach in file_patch_map
		#	patch(id)
		# foreach section where file =
		# 	section(id)
