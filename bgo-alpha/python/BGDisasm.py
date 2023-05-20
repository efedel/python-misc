#!/usr/bin/python
'''
	Big O Disassembler Class

	This defines the virtual disassembler class 
'''
#-------------------------------------------------------------------------
# Disassembler

# --bgo--
import BGModule
import primitives.disasm as disasm

class Disasm(disasm.Disasm):
	def __init__(self, options=0):
		disasm.Disasm.__init__(self, options)

	
# TODO: add operations on DB representation here
