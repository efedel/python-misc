#!/usr/bin/python

import time
import sys
sys.path.append(".")
import task_modules.queue as TaskQueue

class Task(object):
	def __init__(self, str='foo'):
		self._str = str

	def run(self):
		print 'VAL: ' + self._str + '\n'
		
		
if __name__ == '__main__':
	q = TaskQueue.TaskQueue(3)
	
	for i in range(0, 20):
		t = Task(str(i))
		print 'ADD ' + str(i) + ' PRIORITY ' + str(i % 5)
		q.add(t, i % 5)

	time.sleep(5)
	q.shutdown()

	sys.exit(0)
