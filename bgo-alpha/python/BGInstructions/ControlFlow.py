#!/usr/bin/python
'''
	Big O Control Flow Instruction Class
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Control Flow Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_CONTROLFLOW
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def branch_addr(self, vm=None):
		return self._operands[0].to_address(vm)

class BranchCond(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 17
		Instruction.__init__(self, self.TYPE_JCC, section, db_id)

class BranchAlways(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 18
		Instruction.__init__(self, self.TYPE_JMP, section, db_id)

	def next_addr():
		'''  JMP instructions have no next addr '''
		return None

class CallAlways(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 19
		Instruction.__init__(self, self.TYPE_CALL, section, db_id)

class CallCond(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 20
		Instruction.__init__(self, self.TYPE_CALLCC, section, db_id)

class Return(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 21
		Instruction.__init__(self, self.TYPE_RETURN, section, db_id)

	def next_addr(self):
		'''  RET instructions have no next addr '''
		return None

	def branch_addr(self, vm=None):
		'''  RET instructions have no branch addr '''
		return None
