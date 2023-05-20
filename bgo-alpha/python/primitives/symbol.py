#!/usr/bin/python
'''
	Base Symbol class
'''

class Symbol:

	def __init__(self):
		self.__name = name
		self.__offset = offset	# offset from start of section
		self.__section = section

	def file_offset(self):
		pass

	def load_address(self):
		pass
