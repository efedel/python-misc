#!/usr/bin/python
'''
	Big O Stack Instruction Class
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Stack Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_STACK
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def stack_apply(self, vm=None):
		''' apply changes to VM stack and regs '''
		pass

class Push(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 33
		Instruction.__init__(self, self.TYPE_PUSH, section, db_id)

	def stack_apply(self, vm=None):
		pass

class Pop(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 34
		Instruction.__init__(self, self.TYPE_POP, section, db_id)

	def stack_apply(self, vm=None):
		pass

class PushRegisters(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 35
		Instruction.__init__(self, self.TYPE_PUSHREGS, section, db_id)

	def stack_apply(self, vm=None):
		pass

class PopRegisters(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 36
		Instruction.__init__(self, self.TYPE_POPREGS, section, db_id)

	def stack_apply(self, vm=None):
		pass

class PushFlags(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 37
		Instruction.__init__(self, self.TYPE_PUSHFLAGS, section, db_id)

	def stack_apply(self, vm=None):
		pass

class PopFlags(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 38
		Instruction.__init__(self, self.TYPE_POPFLAGS, section, db_id)

	def stack_apply(self, vm=None):
		pass

class EnterFrame(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 39
		Instruction.__init__(self, self.TYPE_ENTER, section, db_id)

	def stack_apply(self, vm=None):
		pass

class LeaveFrame(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 40
		Instruction.__init__(self, self.TYPE_LEAVE, section, db_id)

	def stack_apply(self, vm=None):
		pass
