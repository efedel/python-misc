#!/usr/bin/python
'''
	Big LoadStore Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Load/Store Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_LOADSTORE
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class Move(Instruction):
	''' a load or a store '''
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 22
		Instruction.__init__(self, self.TYPE_MOV, section, db_id)

	def eval(self, vm=None):
		pass


class MoveCond(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 23
		Instruction.__init__(self, self.TYPE_MOVCC, section, db_id)

	def eval(self, vm=None):
		pass

class Exchange(Instruction):
	''' like a move, but with two destinations! '''
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 24
		Instruction.__init__(self, self.TYPE_XCHG, section, db_id)

	def eval(self, vm=None):
		pass

class ExchangeCond(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 25
		Instruction.__init__(self, self.TYPE_XCHGCC, section, db_id)

	def eval(self, vm=None):
		pass
