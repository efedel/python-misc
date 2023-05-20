#!/usr/bin/python
'''
	Big O Compare Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Compare Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_COMPARE
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class Compare(Instruction):
	''' A SUB insn with no dest (results are discarded) '''
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 15
		Instruction.__init__(self, self.TYPE_CMP, section, db_id)

	def eval(self, vm=None):
		pass


class Test(Instruction):
	''' An AND insn with no dest '''
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 16
		Instruction.__init__(self, self.TYPE_TEST, section, db_id)

	def eval(self, vm=None):
		pass
