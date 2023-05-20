#!/usr/bin/python
'''
	Big O Constant class
'''

# --bgo--
import primitives.constant as constant
import dbobject

class Constant(constant.Constant, dbobject.DBObject):

	def __init__(self, db_id=None):

		dbobject.DBObject.__init__(self, id=db_id)

		constant.Constant.__init__(self)

		self.autosave()
