#!/usr/bin/python
'''
	Big O Arithmetic Instruction Class
'''
# --bgo--
import BGInstruction as insn

#-------------------------------------------------------------------------
# Arithmetic Instruction

class Instruction(insn.Instruction):
	def __init__(self, type, section=None, db_id=None):
		insn.Instruction.__init__(self, section, db_id)
		if db_id is not None:
			return
		self._major_type = self.GROUP_ARITHMETIC
		self._minor_type = type
		self.dirty()

	# Additions to the BGInstruction interface
	def eval(self, vm=None):
		pass

class Add(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 1
		Instruction.__init__(self, self.TYPE_ADD, section, db_id)

	def eval(self, vm=None):
		pass

class Sub(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 2
		Instruction.__init__(self, self.TYPE_SUB, section, db_id)

	def eval(self, vm=None):
		pass

class Mul(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 3
		Instruction.__init__(self, self.TYPE_MUL, section, db_id)

	def eval(self, vm=None):
		pass

class Div(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 4
		Instruction.__init__(self, self.TYPE_DIV, section, db_id)

	def eval(self, vm=None):
		pass

class ShiftLeft(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 5
		Instruction.__init__(self, self.TYPE_SHL, section, db_id)

	def eval(self, vm=None):
		pass

class ShiftRight(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 6
		Instruction.__init__(self, self.TYPE_SHR, section, db_id)

	def eval(self, vm=None):
		pass
	
class AbsoluteVal(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 7
		Instruction.__init__(self, self.TYPE_ABS, section, db_id)

	def eval(self, vm=None):
		pass

class SquareRoot(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 8
		Instruction.__init__(self, self.TYPE_SQRT, section, db_id)

	def eval(self, vm=None):
		pass

class Tangent(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 9
		Instruction.__init__(self, self.TYPE_TAN, section, db_id)

	def eval(self, vm=None):
		pass

class Sine(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 10
		Instruction.__init__(self, self.TYPE_SINE, section, db_id)

	def eval(self, vm=None):
		pass

class Cosine(Instruction):
	def __init__(self, section=None, db_id=None):
		self._class_db_id = 11
		Instruction.__init__(self, self.TYPE_COSINE, section, db_id)

	def eval(self, vm=None):
		pass

