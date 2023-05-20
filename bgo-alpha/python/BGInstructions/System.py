#!/usr/bin/python
'''
	Big O System Instruction Classes
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# System Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_SYSTEM
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class IOPortRead(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 41
		Instruction.__init__(self, self.TYPE_IN, section, db_id)

class IOPortWrite(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 42
		Instruction.__init__(self, self.TYPE_OUT, section, db_id)

class CpuID(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 43
		Instruction.__init__(self, self.TYPE_CPUID, section, db_id)

class Halt(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 44
		Instruction.__init__(self, self.TYPE_HALT, section, db_id)

class SysCtl(Instruction):
	''' unknown system/privileged instruction '''
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 45
		Instruction.__init__(self, self.TYPE_SYSCTL, section, db_id)
	
