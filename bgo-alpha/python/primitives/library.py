#!/usr/bin/python
'''
	Big O File Container (Library) class
'''

# --bgo--
import dbobject

class Library(dbobject.DBObject):
	
	def __init__(self):
		self.__symbols = set.Set()
		self.__name = name
