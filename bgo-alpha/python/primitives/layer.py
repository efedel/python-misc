#!/usr/bin/python

'''
	Base Layer class
'''

class Layer(object):
	'''
		Methods:

		Members:
			__name (str)
			__layers (list)
	'''

	def __init__(self, name):
		self._name = name
