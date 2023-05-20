#!/usr/bin/python
'''
	Big O X86 Disassembler module

	Instruction definitions
'''

# --bgo-- 
from disasm_modules.x86_Classes.x86Enum import *
# --bgo instruction types--
import BGInstructions.Arithmetic as Arith
import BGInstructions.Bit as Bit
import BGInstructions.Compare as Compare
import BGInstructions.ControlFlow as CFlow
import BGInstructions.LoadStore as LodStor
import BGInstructions.Logic as Logic
import BGInstructions.Misc as Misc
import BGInstructions.Stack as Stack
import BGInstructions.System as System
import BGInstructions.Trap as Trap


# ============================================================================
# instruction classes specific to x86 CPUs
class PushRegs(Stack.Instruction):
	__type = TYPE_PUSHREGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PopRegs(Stack.Instruction):
	__type = TYPE_POPREGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PushFlags(Stack.Instruction):
	__type = TYPE_PUSHFLAGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class PopFlags(Stack.Instruction):
	__type = TYPE_POPFLAGS

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Stack.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrCmp(Compare.Instruction):
	__type = TYPE_STRCMP

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Compare.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrLoad(LodStor.Instruction):
	__type = TYPE_STRLOAD

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrMove(LodStor.Instruction):
	__type = TYPE_STRMOV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class StrStore(LodStor.Instruction):
	__type = TYPE_STRSTORE

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class SetFlag(Bit.Instruction):
	__type = TYPE_FLAGSET

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class ClearFlag(Bit.Instruction):
	__type = TYPE_FLAGCLEAR

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class ToggleFlag(Bit.Instruction):
	__type = TYPE_FLAGTOG

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Bit.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class LoadPi(LodStor.Instruction):
	__type = TYPE_LDPI

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class LoadZero(LodStor.Instruction):
	__type = TYPE_LDZ

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		LodStor.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class RotateLeft(Arith.Instruction):
	__type = TYPE_ROL

	''' This will differ from ShiftLeft in its eval() '''
	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Arith.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class RotateRight(Arith.Instruction):
	__type = TYPE_ROR

	''' This will differ from ShiftRight in its eval() '''
	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Arith.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class BcdConv(Misc.Instruction):
	__type = TYPE_BCDCONV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class SizeConv(Misc.Instruction):
	__type = TYPE_SZCONV

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

class Xlat(Misc.Instruction):
	__type = TYPE_TRANSLATE

	def __init__(self, section=None):
		global x86_module
		self._class_db_id = x86_module._classes[self.__type]
		Misc.Instruction.__init__(self, 
			x86_module.type(self.__type), section)

	def eval(self, vm=None):
		pass

