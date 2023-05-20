#!/usr/bin/python
'''
	Big O File Section Class
'''

# --bgo--
import dbobject
import primitives.section as section

# TODO: classes for section types?
class Section(section.Section,dbobject.DBObject):
	def __init__(self, file=None, name=None, offset=0, size=0, 
			load_addr=0, endian=section.Section.ENDIAN_BIG, 
			word_size=1, arch=None, db_id=None):
		# initialize database representation
		dbobject.DBObject.__init__(self, id=db_id)
		if db_id is not None:
			# section has been restored from database
			return

		section.Section.__init__(self, file, name, offset, size, 
					 load_addr, endian, word_size,
					 arch )
		
		self.autosave()
	# ==============================================
	# DisasmBuf API Overrides
	def add_insn(self, insn):
		section.Section.add_insn(self, insn)
		self.autosave()

	# ==============================================
	# Section API Overrides
	def disassemble(self):
		#self.db().begin()
		section.Section.disassemble(self)
		self.autosave()
		#self.db().commit()

	def rename(self, str):
		section.Section.rename(self, str)
		self.autosave()

	def set_flag(self, str):
		section.Section.set_flag(self, str)
		self.autosave()

	def clear_flag(self, str):
		section.Section.clear_flag(self, str)
		self.autosave()

	def add_data(self, data):
		section.Section.add_data(self, data)
		self.autosave()

	def add_symbol(self, sym):
		section.Section.add_symbol(self, sym)
		self.autosave()


	# ==============================================
	# DBObject Interface
	def __save(self):
		flag_str = self.flags_str()
		
		if not self.db_id():
			# insert into db
			file_id = self.file().db_id()
			self._db_id = self.db().insert('section',
				{ 'file' : file_id,
				  'type' : self._type[1],
				  'name' : self.name(),
				  'flags' : flag_str,
				  'access' : self.access(),
				  'file_offset' : self.offset(),
				  'load_addr' : self.load_addr(),
				  'size ' : self.size(),
				  'arch' : self._arch[1],
				  'compiler' : self._compiler[1],
				  'source' : self._lang[1] } )
		else:
			self.db().update('section', self.db_id(),
				{ 'type' : self._type[1],
				  'name' : self.name(),
				  'flags' : flag_str,
				  'access' : self.access(),
				  'arch' : self._arch[1],
				  'compiler' : self._compiler[1],
				  'source' : self._lang[1] } )
		self._dirty = 0

	def save(self):
		if self._dirty :
			self.__save()
		
		for i in self._insn:
			i.save()
		
		for d in self._data:
			d.save()
		
		for s in self._symbols:
			s.save()

	def delete(self):
		dbobject.DBObject.delete(self)
		
		for i in self._insn:
			i.delete()
		
		for d in self._data:
			d.delete()
		
		for s in self._symbols:
			s.delete()

	def restore(self, db_id, values=None):
		pass

