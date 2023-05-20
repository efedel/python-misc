#!/usr/bin/python
'''
	Big O Bit Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Bit Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_BIT
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def flag_operand(self):
		return self._flag_operand

	def eval(self, vm=None):
		''' perform operation on eflags '''
		pass

class Set(Instruction):
	def __init__(self, flag, section=None, db_id=None):
		self._class_db_id = 12
		Instruction.__init__(self, self.TYPE_SET_BIT, section, db_id)

	def eval(self, vm=None):
		pass

class Clear(Instruction):
	def __init__(self, flag, section=None, db_id=None):
		self._class_db_id = 13
		Instruction.__init__(self, self.TYPE_CLEAR_BIT, section, db_id)

	def eval(self, vm=None):
		pass

class Toggle(Instruction):
	def __init__(self, flag, section=None, db_id=None):
		self._class_db_id = 14
		Instruction.__init__(self, self.TYPE_TOGGLE_BIT, section, db_id)

	def eval(self, vm=None):
		pass
