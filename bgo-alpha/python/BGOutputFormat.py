#!/usr/bin/python
'''
	Big O Assembler virtual class
'''

# -- bgo--
import BGModule
import primitives.assembler as assembler

class Assembler(assembler.Assembler):
	def __init__(self, options=""):
		assembler.Assembler.__init__(self, options)

		# TODO:
		# Insert assembler-specific rows into DB
