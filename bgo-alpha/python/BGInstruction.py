#!/usr/bin/python
'''
	Big O Instruction Class
'''
# --bgo--
import dbobject
import primitives.instruction as insn

insn_def_cache = {}

def cache_add(key, id):
		'''
			add insn_def id under key [insn signature]
		'''
		insn_def_cache[str(key)] = id
		#insn_def_cache.append( (str(key),id) )
		#insn_def_cache.sort()
	
def cache_lookup(key):
		
		return insn_def_cache.get(str(key), None)
		#result = [ x[1] for x in insn_def_cache if x[0] == str(key) ]
		#if result == []:
		#	return None
		#return result[0]
	
#-------------------------------------------------------------------------
# Instruction

class Instruction(insn.Instruction, dbobject.DBObject):
	def __init__(self, section=None, db_id=None):
		# initialize database representation
		dbobject.DBObject.__init__(self, id=db_id)
		if db_id is not None:
			# restore has already been handled
			return
		
		insn.Instruction.__init__(self, section)
		
		# Instruction Definition in DB
		self._insn_def_id = 0
		
		#self.autosave()
		self.dirty()

	# Instruction API Overrides
	def add_operand(self, operand):
		insn.Instruction.add_operand(self, operand)

		self.autosave()

	# DB Object Interface
	def __get_insn_def(self):
		# first check cache
		id = cache_lookup(self.signature())
		if id is not None:
			self._insn_def_id = id
			return
		
		# build the operand WHERE clause
		op_count = 0
		op_clause = ''
		
		for o in self._operands:
			op_count += 1
			buf = "(ord = " + str(o.order()) + " AND op_def = " + \
				str(o._op_def_id) + " AND datatype = " + \
				str(o._datatype[1]) + ")"
			if op_clause == '':
				op_clause = buf
			else:
				op_clause = op_clause + ' OR ' + buf
		
		if op_count > 1:
			# enclose all these ORs in parens , just in case
			op_clause = "(" + op_clause + ")"

		if op_clause != '':
			# only use the AND when there are 1 or more operands
			op_clause = ' AND ' + op_clause
		
		# check if a def for this mnemonic and prefixes
		# exists, and does it have exactly the same operands
		# mapped to it
		
		where_str = "i.mnemonic = '" + self.mnemonic() + \
			"' AND i.prefixes = '" + self.prefix_str() + \
			"' AND " + str(op_count) + " = ( SELECT count(*) " + \
			"FROM insn_op_def_map m WHERE m.insn_def = i.id " + \
			op_clause + ")"

		id = self.db().fetch_id_where('insn_def i', where_str, 'i')
		
		if not id:
			#print "WHERE: " + where_str
			#print "INSN_DEF " + self.mnemonic() + str(self._bytes)
			
			# if not, create the definition
			id = self.db().insert('insn_def',
				{ 'major_type' : self._major_type[1] ,
				  'minor_type' : self._minor_type[1] ,
				  'mnemonic' : self.mnemonic() ,
				  'flags_set': self.flags_set_str(),
				  'flags_tested' : self.flags_tested_str(), 
				  'prefixes' : self.prefix_str(), 
				  'prefix_mnemonic' : self.prefix_mnemonic(),
				  'bytes' : self.db().blob(self.bytes()),
				  'signature': self.db().blob(self.signature()),
				  'size' : self.size(),
				  'stack_mod' : self.stack_mod(),
				  'cpu' : self._cpu[1],
				  'isa' : self._isa[1],
				  'class' : self._class_db_id,
				  'title' : self.title(),
				  'description': self.description(),
				  'pseudocode' : self.pseudocode()} )
			
			# ...and map the operand definitions to it
			for o in self._operands:
				o._insn_map_insert(id)
			
		self._insn_def_id = id
		cache_add(self.signature(), id)

	def __save(self):
		if not self.db_id():
			# check if instruction defintion exists
			if not self._insn_def_id:
				# get DB id for insn definition
				self.__get_insn_def()
			
			# insert new instruction row
			self._db_id = self.db().insert( 'instruction',
				{ 'insn_def' : self._insn_def_id,
				  'file_offset' : self.offset(),
				  'address' : self.address()} )
			
		else:
			# update existing instruction row
			# NOTE: this can only be used to change the
			# instruction def -- everything else is constant --
			# therefore we force an insn_def id fetch
			self.__get_insn_def()
			
			self.db().update( 'instruction', self._db_id,
				{ 'insn_def' : self._insn_def_id} )
		
		self._dirty = 0

	def save(self):
		#self.db().begin()
		# create rows for all operands
		for o in self._operands:
			o.save()
		
		if self._dirty:
			self.__save()
		#self.db().commit()
	
	def delete(self):
		# delete from operand-code mapping
		
		# delete from insn instance
		
		pass
	
	def restore(self, db_id, values=None):
		# if values restore from values, return
		# get code instance
		# get operand instances
		# get operand objects
		# get insn object
		pass
	
	def __db_values(self):
		pass

