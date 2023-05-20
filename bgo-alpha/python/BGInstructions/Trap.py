#!/usr/bin/python
'''
	Big O Trap Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Trap Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_TRAP
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def trap(self, os=None):
		pass
		
class Trap(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 46
		Instruction.__init__(self, TYPE_TRAP, section, db_id)

	def trap(self, os=None):
		pass
		
class TrapCond(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 47
		Instruction.__init__(self, TYPE_TRAPCC, section, db_id)

	def trap(self, os=None):
		pass
		
class TrapReturn(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 48
		Instruction.__init__(self, TYPE_TRET, section, db_id)

	def trap(self, os=None):
		pass
		
class Bound(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 49
		Instruction.__init__(self, TYPE_BOUND, section, db_id)

	def trap(self, os=None):
		pass
		
class Debug(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 50
		Instruction.__init__(self, TYPE_DEBUG, section, db_id)

	def trap(self, os=None):
		pass
		
class Trace(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 51
		Instruction.__init__(self, TYPE_TRACE, section, db_id)

	def trap(self, os=None):
		pass
	
class InvalidOpcode(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id = 52
		Instruction.__init__(self, TYPE_INVALID_OP, section, db_id)

	def trap(self, os=None):
		pass
		
class Overflow(Instruction):
	def __init__(self, type, section=None, db_id=None):
		self._class_db_id =53
		Instruction.__init__(self, TYPE_OFLOW, section, db_id)

	def trap(self, os=None):
		pass
