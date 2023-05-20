#!/usr/bin/python
'''
	Big O Logic Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Logic Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_LOGIC
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class And(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 26
		Instruction.__init__(self, self.TYPE_AND, section, db_id)

	def eval(self, vm=None):
		pass

class Or(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 27
		Instruction.__init__(self, self.TYPE_OR, section, db_id)

	def eval(self, vm=None):
		pass

class Xor(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 28
		Instruction.__init__(self, self.TYPE_XOR, section, db_id)

	def eval(self, vm=None):
		pass

class Not(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 29
		Instruction.__init__(self, self.TYPE_NOT, section, db_id)

	def eval(self, vm=None):
		pass

class Neg(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 30
		Instruction.__init__(self, self.TYPE_NEG, section, db_id)

	def eval(self, vm=None):
		pass

