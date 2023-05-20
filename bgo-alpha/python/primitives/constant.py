#!/usr/bin/python
'''
	Base Constant class
'''

class Constant(object):

	def __init__(self, name=None, value=None, namespace=None):
		self._name = name
		self._value = value
		if namespace is None:
			namespace = self.DEFAULT_NAMESPACE

	def name(self):
		pass

	def value(self):
		pass

class Namespace(object):
