#!/usr/bin/python
'''
	Big O Instruction Operand Class
'''

# --bgo--
import dbobject
import primitives.operand as op

op_def_cache = {}

def def_cache_add(key, id):
	op_def_cache[key] = id

def def_cache_lookup(key):
	return op_def_cache.get(key, None)
op_val_cache = {}

def val_cache_add(key, id):
	op_val_cache[key] = id

def val_cache_lookup(key):
	return op_val_cache.get(key, None)

#-------------------------------------------------------------------------
# Operand
class Operand(op.Operand, dbobject.DBObject):
	
	def __init__(self, insn=None, order=None, type=None, db_id=None):
		dbobject.DBObject.__init__(self, id=db_id)

		if db_id is not None:
			# object has been restored from db
			return
		
		op.Operand.__init__(self, insn, order, type)
		
		# NOTE: self._db_id is row in insn_op_def_map
		# id of Operand Definition in DB
		self._op_def_id = 0
		# id of Operand Definition Value in DB
		self._op_val_id = 0

		self.dirty()
		#self.autosave()

	def _get_op_def(self):
		return 0

	def _get_register_id(self, reg):
		id = self.db().fetch_id('op_reg', 
			{'reg_id' : str(reg.id()) } )

		if id:
			return id
		# else: need to create register definiton

		alias = reg.alias()
		if alias is not None:
			alias_id = self._get_register_id(alias)
		else:
			alias_id = None
			
		# insert op value def into op_reg table
		id = self.db().insert( 'op_reg', 
				{ 'reg_id' : reg.id(),
				  'mnemonic' : reg.mnemonic(),
				  'type' : reg.type_str(),
				  'size': reg.size(),
				  'alias' : alias_id,
				  'alias_shift' : reg.alias_shift() } )
		return id

	def _insn_map_insert(self, insn_id):
		self._db_id = self.db().insert('insn_op_def_map',
			{ 'insn_def' : insn_id,
			  'op_def' : self._op_def_id,
			  'name' : self.name(),
			  'datatype' : self._datatype[1],
			  'flags' : self.flags_str(),
			  'size' : self.size(),
			  'ord' : self.order(),
			  'access' : self.access()} )
		# this is the last modification made by insn
		# during insn/operand insert, so clear dirty flag:
		# there are no more changes to save
		self._dirty = 0
	
	def save(self):
		if not self._dirty:
			return
		
		# If operand def has not been set
		if not self._op_def_id:
			self._get_op_def()
		
		# If insn has created mapping...
		if self.db_id():
			# update map row contents with changes
			self.db().update('insn_op_def_map', self.db_id(),
			{ 'name' : self._name(),
			  'datatype' : self._datatype[1],
			  'flags' : self.flags_str(),
			  'size' : self.size()} )
			
			self._dirty = 0
			
		else:
			# else do nothing: wait for insn to create map
			pass
	
	def delete(self):
		pass

	def restore(self):
		pass
	
	def resolve(self, vm):
		''' use BGVirtualMachine vm to resolve operand to an address'''
		pass
#-------------------------------------------------------------------------
class Immediate(op.Immediate, Operand):

	def __init__(self, insn=None, order=None, val=None, 
			type=Operand.TYPE_IMM, db_id=None):

		# Initialize DBObject and autosave
		Operand.__init__(self, insn, order, type)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Immediate.__init__(self, insn, order, val)

	def apply_constant(self, constant):
		
		op.Immediate.apply_constant(self, constant)
		
		self.autosave()

	def remove_constant(self):
		
		op.Immediate.remove_constant(self)
		
		self.autosave()

	def _get_op_def(self):
		#val_key = 'op_imm' + str(self.value())

		#id = val_cache_lookup(val_key)
		#if id is not None:
		#	self._op_val_id = id
		#	def_key = 'op_def' + str(id)
		#	self._op_def_id = def_cache_lookup(id)
		#	return

		id = self.db().fetch_id('op_imm', 
			{ 'value' : str(self.value()) } )
		
		if id:
			self._op_val_id = id
			self._op_def_id = self.db().fetch_id('op_def', 
				{ 'value' : str(id) } )
		else:
			# insert op value def into op_imm table
			self._op_val_id = self.db().insert( 'op_imm', 
				{ 'value' : self.value() } )
			
			# insert link to value in op_def table
			self._op_def_id = self.db().insert( 'op_def',
				{ 'type' : self._type[1],
				  'value' : self._op_val_id } )

		#val_cache_add(val_key, self._op_val_id)
		#def_key = 'op_def' + str(self._op_val_id)
		#def_cache_add(def_key, self._op_def_id)
	
	def restore(self):
		pass

	def resolve(self, vm):
		# immediate values are assumed to be addresses
		return self.value()

#-------------------------------------------------------------------------
class Relative(op.Relative, Immediate):

	def __init__(self, insn=None, order=None, type=None, val=0, 
			offset=0, address=0, db_id=None):

		# Initialize DBObject and autosave
		Immediate.__init__(self, insn, order, val, type, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Relative.__init__(self, insn, order, type, 
			val, offset, address)

	def apply_constant(self, constant):
		
		op.Relative.apply_constant(self, constant)
		
		self.autosave()

	def remove_constant(self):
		
		op.Relative.remove_constant(self)
		
		self.autosave()
	
	def _get_op_def(self):
		id = self.db().fetch_id('op_rel', 
			{ 'value' : str(self.value()),
			  'address' : self.address() } )
		
		if id:
			self._op_val_id = id
			self._op_def_id = self.db().fetch_id('op_def', 
				{ 'value' : str(id) } )
		else:
			# insert op value def into op_imm table
			self._op_val_id = self.db().insert( 'op_rel', 
				{ 'value' : self.value(),
				  'file_offset' : self.offset(),
				  'address' : self.address() } )
			
			# insert link to value in op_def table
			self._op_def_id = self.db().insert( 'op_def',
				{ 'type' : self._type[1],
				  'value' : self._op_val_id } )

	def restore(self):
		pass
	
	def resolve(self, vm):
		# relative values have address pre-calculated
		return self.address()

#-------------------------------------------------------------------------
class Offset(op.Offset, Immediate):

	def __init__(self, insn=None, order=None, val=0, db_id=None):

		# Initialize DBObject and autosave
		Immediate.__init__(self, insn, order, val, 
					Operand.TYPE_OFFSET, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Offset.__init__(self, insn, order, val)

	def apply_constant(self, constant):
		
		op.Offset.apply_constant(self, constant)
		
		self.autosave()

	def remove_constant(self):
		
		op.Offset.remove_constant(self)
		
		self.autosave()
	
	def restore(self):
		pass

#-------------------------------------------------------------------------
class Address(op.Address, Immediate):

	def __init__(self, insn=None, order=None, val=None, db_id=None):

		# Initialize DBObject and autosave
		Immediate.__init__(self, insn, order, val, 
			Operand.TYPE_ABSOLUTE, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Address.__init__(self, insn, order, val)

	def apply_constant(self, constant):
		
		op.Address.apply_constant(self, constant)
		
		self.autosave()

	def remove_constant(self):
		
		op.Address.remove_constant(self)
		
		self.autosave()

	def restore(self):
		pass


#-------------------------------------------------------------------------
class EffectiveAddress(op.EffectiveAddress, Operand):

	def __init__(self, insn=None, order=None, disp=None, base=None, \
			index=None, scale=None, alias_shift=0, db_id=None):

		# Initialize DBObject and autosave
		Operand.__init__(self, insn, order, Operand.TYPE_EXPR, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.EffectiveAddress.__init__(self, insn, order, disp,
			base, index, scale)

	def apply_constant(self, constant, 
			   to=op.EffectiveAddress.EADDR_DISP):
		
		op.EffectiveAddress.apply_constant(self, constant, to)
		
		self.autosave()

	def remove_constant(self, part=op.EffectiveAddress.EADDR_DISP):
		
		op.EffectiveAddress.remove_constant(self, part)
		
		self.autosave()

	def _get_op_def(self):
		cond = []
		
		base = self.base()
		base_id = None
		if base is not None:
			base_id = self._get_register_id(base)
			cond.append( 'base = ' + str(base_id) )
		
		index = self.index()
		idx_id = None
		if index is not None:
			idx_id = self._get_register_id(index)
			cond.append( 'idx = ' + str(idx_id) )
		
		scale = self.scale()
		if scale > 1:
			cond.append( 'scale = ' + str(scale) )
		
		disp = self.disp()
		if disp is not None:
			cond.append( 'disp = ' + str(disp) )
		
		where_clause = ''
		for c in cond:
			if where_clause == '':
				where_clause = c
			else:
				where_clause = where_clause + ' AND ' + c
		
		id = self.db().fetch_id_where('op_expr', where_clause )
		
		if id:
			self._op_val_id = id
			self._op_def_id = self.db().fetch_id('op_def', 
				{ 'value' : str(id) } )
		else:
			# insert op value def into op_expr table
			self._op_val_id = self.db().insert( 'op_expr', 
				{ 'base' : base_id,
				  'idx' : idx_id,
				  'scale' : scale,
				  'disp' : disp } )
			
			# insert link to value in op_def table
			self._op_def_id = self.db().insert( 'op_def',
				{ 'type' : self._type[1],
				  'value' : self._op_val_id } )
		
	def restore(self):
		pass
	
	def resolve(self, vm):
		if vm is None:
			# no way to determine this address
			return self.INVALID_ADDR
		# TODO: FIX
		return self.INVALID_ADDR

#-------------------------------------------------------------------------
class Register(op.Register, Operand):

	def __init__(self, insn=None, order=None, id=None, mnemonic=None, \
			type=None, size=None, alias=None, alias_shift=0, \
			db_id=None):

		# Initialize DBObject and autosave
		Operand.__init__(self, insn, order, Operand.TYPE_REG, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Register.__init__(self, insn, order, id, mnemonic,
			type, size, alias, alias_shift)

	def apply_constant(self, constant):
		op.Register.apply_constant(self, constant)
	
		self.autosave()

	def remove_constant(self):
		op.Register.remove_constant(self)
		self.autosave()

	def _get_op_def(self):
		id = self._get_register_id(self)
		
		self._op_val_id = id
		self._op_def_id = self.db().fetch_id('op_def', 
			{ 'value' : str(id) } )
		
		if not self._op_def_id :
			# insert link to value in op_def table
			self._op_def_id = self.db().insert( 'op_def',
				{ 'type' : self._type[1],
				  'value' : self._op_val_id } )
	
	def restore(self):
		pass

	def resolve(self, vm):
		if vm is None:
			# no way to determine address for reg
			return self.INVALID_ADDR
		return vm.reg_read(self.Register)

class Bit(op.Bit, Operand):

	def __init__(self, insn=None, order=None, position=None, 
			name=None, db_id=None):
		# Initialize DBObject and autosave
		Operand.__init__(self, insn, order, Operand.TYPE_BIT, db_id)

		if db_id is not None:
			# object has been restored from database
			return
		
		op.Bit.__init__(self, insn, order, position, name)

	def _get_op_def(self):
		raise AssertionError, 'Attempt to INSERT Bit Operand'
		# this should never be called : the disasm module
		# should have the _db_id for these operands
		# set to DB rows it inserts.
		id = self.db().fetch_id('op_bit', 
			{ 'position' : str(self.position()),
			  'mnemonic' : self.mnemonic() } )
		
		if id:
			self._op_val_id = id
			self._op_def_id = self.db().fetch_id('op_def', 
				{ 'value' : str(id) } )
		else:
			# insert op value def into op_ table
			self._op_val_id = self.db().insert( 'op_bit', 
				{ 'position' : self.position(),
				  'mnemonic' : self.mnemonic() } )
			
			# insert link to value in op_def table
			self._op_def_id = self.db().insert( 'op_def',
				{ 'type' : self._type[1],
				  'value' : self._op_val_id } )
	
	def restore(self):
		pass

	def resolve(self, vm):
		# It is impossible for a bit to contain a valid address
		return self.INVALID_ADDR
