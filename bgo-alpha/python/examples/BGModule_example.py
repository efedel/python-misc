#!/usr/bin/python
'''
	Big O example module
'''

import sys
sys.path.append(".")
# -- bgo --
import BGModule
import dbobject

MODULE_VERSION = 0.1
MODULE_NAME = 'example'
MODULE_AUTHOR = 'mammon_'
MODULE_LICENSE = 'LGPL'


class ExampleModule(BGModule.Module):
	def __init__(self):
		BGModule.Module.__init__(self, MODULE_NAME, MODULE_VERSION,
					MODULE_AUTHOR, MODULE_LICENSE)
	def new_install(self):
		pass
	def upgrade_install(self):
		pass

class Example(DBObject):
	
	bg_module = None

	def __init__(self, db_id=None):
		if self.bg_module is None:
			Example.bg_module = ExampleModule()
