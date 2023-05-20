#!/usr/bin/python
'''
	Big O Symbol class
'''

# --bgo-- 
import primitives.symbol as symbol
import dbobject

class Symbol(symbol.Symbol, dbobject.DBObject):

	def __init__(self):

		symbol.Symbol.__init__(self)

		dbobject.DBObject.__init__(self)

		self.autosave()
