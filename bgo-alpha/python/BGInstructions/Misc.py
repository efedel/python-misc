#!/usr/bin/python
'''
	Big O Misc Instruction Class
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Misc Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, flag, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_MISC
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class Nop(Instruction):
	def __init__(self, flag, section=None, db_id=None):
		self._class_db_id = 31
		Instruction.__init__(self, self.TYPE_NOP, section, db_id)

class Unknown(Instruction):
	def __init__(self, flag, section=None, db_id=None):
		self._class_db_id = 32
		Instruction.__init__(self, self.TYPE_UNK, section, db_id)
